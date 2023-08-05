"""
Defines the pipeline before a FileTree is provided.

A pipeline is a collection of functions with mapping from the function parameters to input/output/reference/placeholder basenames.
"""
from typing import List, Optional, Set, Tuple, Dict, Collection, Callable, Union, Any
import argparse
from dataclasses import dataclass
from file_tree import FileTree
from file_tree.file_tree import is_singular
import numpy as np
from copy import copy
import inspect
import xarray
from collections import namedtuple
from fsl_sub import submit
from file_tree.template import is_singular
from pathlib import Path
import graphviz
import fnmatch
try:
    import datalad
except ImportError:
    datalad = None

class Pipeline:
    """Collection of python functions forming a pipeline.

    You can either create a new pipeline (`from fsl_pipe import Pipeline; pipe = Pipeline()`) or use a pre-existing one (`from fsl_pipe import pipe`)

    Scripts are added to a pipeline by using the pipeline as a decorator (see :meth:`__call__`).

    To run the pipeline based on instructions from the command line run :meth:`pipe.cli(tree) <cli>`, 
    where tree is a FileTree defining the directory structure of the pipeline input & output files.

    :ivar scripts: list of :class:`PipedFunction`, which define the python functions forming the pipeline and their input/output templates
    """

    def __init__(self, scripts=None, default_output=None, default_submit=None):
        """Create a new empty pipeline."""
        if scripts is None:
            scripts = []
        if default_output is None:
            default_output = []
        if default_submit is None:
            default_submit = {}
        self.scripts: List[PipedFunction] = list(scripts)
        self.default_output: List[str] = list(default_output)
        check_submit_parameters(default_submit)
        self.default_submit = default_submit

    def __call__(self, function=None, *, kwargs=None, no_iter=None, placeholders=None, as_path=False, submit=None, batch=None):
        """Add a python function as a :class:`PipedFunction` to the pipeline.

        This is the main route through which jobs are added to the pipeline.

        .. code-block:: python

            from fsl_pipe import pipe, In, Out, Ref, Var

            @pipe(submit=dict(jobtime=40))
            def func(in_path: In, out_path: Out, ref_path: Ref, placeholder_key: Var):
                pass

        :param function: Optionally provide the function directly. This can be useful when not using `pipe` as a decorator, e.g.:
    
            .. code-block:: python

                from fsl_pipe import pipe, In, Out, Ref, Var
                from shutil import copyfile

                pipe(copyfile, kwargs={'src': In('template_in'), 'dst': Out('template_out')})

        :param kwargs: maps function keyword arguments to template names (In/Out/Ref), placeholder names (Var), or anything else. Templates or placeholders are replaced by their values based on the file-tree. Anything else is passed on unaltered.
        :param no_iter: optional set of parameters not to iterate over.
        :param as_path: if set to true, provide template filenames to the function as `pathlib.Path` objects instead of strings.
        :param placeholders: dictionary overriding the placeholders set in the filetree for this specific function. This can, for example, be used to run this function on a sub-set of subjects.
        :param submit: dictionary with the flags to pass on to `fsl_sub.submit`, when submitting jobs to a cluster queue.
        :param batch: label used to batch multiple jobs into one when submitting to the cluster
        """
        if submit is None:
            submit = {}
        submit_params = dict(**self.default_submit, **submit)
        check_submit_parameters(submit_params)
        def wrapper(func):
            self.scripts.append(PipedFunction(func, submit_params=submit_params, kwargs=kwargs, no_iter=no_iter, override=placeholders, as_path=as_path, batch=batch))
            return func
        if function is None:
            return wrapper
        wrapper(function)
        return function

    def generate_jobs(self, tree: FileTree):
        """
        Split the pipeline into individual jobs.

        Produces an unsorted `JobList`, which can be sorted by running `filter` on it.

        :param tree: set of templates for the input/output/reference files with all possible placeholder values
        """
        from .job import JobList, FileTarget
        all_targets: Dict[str, FileTarget] = {}
        jobs = []
        for script in self.scripts:
            jobs.extend(script.get_jobs(tree, all_targets))
        return JobList(tree, jobs, all_targets)

    def default_parser(self, tree: FileTree, parser: Optional[argparse.ArgumentParser]=None, include_vars=None, exclude_vars=()) -> argparse.ArgumentParser:
        """
        Add default `fsl-pipe` arguments to an argument parser (will create a new argument parser if needed).

        :param tree: `file_tree.FileTree` object describing the directory structure for the input/output files (defaults to datalad tree).
        :param parser: Optional argument parser that will be updated with the default `fsl-pipe` arguments (by default a new one is created).
        :param include_vars: if provided, only include expose placeholders in this list to the command line
        :param exclude_vars: exclude placeholders in this list from the command line
        :return: Argument parser with the default `fsl-pipe` arguments. If one was provided as input, that one will be returned.
        """
        from .job import RunMethod
        if parser is None:
            parser = argparse.ArgumentParser(description="Runs the pipeline")
        if len(self.scripts) == 0:
            raise ValueError("The pipeline does not contain any scripts...")
        templates = set.union(*[script.filter_templates(True, tree.template_keys()) for script in self.scripts])

        if len(self.default_output) == 0:
            default_output = list(sorted(templates))
        else:
            default_output = self.default_output

        parser.add_argument("templates", nargs="*", default=default_output,
                            help=f"Set to one or more template keys or file patterns (e.g., \"*.txt\"). Only these templates/files will be produced. If not provided all templates will be produced ({', '.join(default_output)}).")
        parser.add_argument("-m", '--pipeline_method', default=RunMethod.default().name,
                            choices=[m.name for m in RunMethod],
                            help=f"method used to run the jobs (default: {RunMethod.default().name})")
        parser.add_argument("-o", '--overwrite', action='store_true', help="If set overwrite any requested files.")
        parser.add_argument("-d", '--overwrite_dependencies', action='store_true',
                            help="If set also overwrites dependencies of requested files.")
        parser.add_argument("-j", '--job-hold', default='',
                            help='Place a hold on the whole pipeline until job has completed.')
        parser.add_argument('--skip-missing', default='',
                            help='If set skip running any jobs depending on missing data. This replaces the default behaviour of raising an error if any required input data is missing.')
        parser.add_argument("-q", '--quiet', action='store_true', help="Suppresses the report on what will be run (might speed up starting up the pipeline substantially).")
        parser.add_argument("-b", "--batch", action="store_true", help="Batch jobs based on submit parameters and pipeline labels before running them.")
        if datalad is not None:
            parser.add_argument("--datalad", action='store_true',
                                help="run datalad get on all input data before running/submitting the jobs")
        for var, values in tree.placeholders.items():
            if not isinstance(var, str):
                continue
            if '/' in var:
                continue
            if var in exclude_vars:
                continue
            if include_vars is not None and var not in include_vars:
                continue
            if np.asarray(values).ndim == 1:
                default = ','.join([str(v) for v in values])
            else:
                default = str(values)
            parser.add_argument(f"--{var}", nargs='+', help=f"Use to set the possible values of {var} to the selected values (default: {default})")
        return parser

    def run_cli(self, args: argparse.Namespace, tree: FileTree):
        """
        Run the pipeline based on arguments extracted from the default argument parser.

        :param args: Namespace consisting of arguments extracted from the command line (produced by `argparse.ArgumentParser.parse_args`). This is expected to contain:

            - templates (defaults to `self.default_output`): list of which templates the pipeline should produce
            - pipeline_method: string with method used to run the jobs
            - overwrite: boolean, which if true overwrite any requested files
            - overwrite_dependencies: boolean, which if true also overwrites dependencies of requested files
            - job-hold: string with comma-separated list, which contains job(s) that will be waited for
            - skip-missing: whether to skip jobs depending on missing data instead of raising an error
            - datalad (defaults to False): if true, run datalad get on all input data before running/submitting the jobs
            - {placeholder} (defaults to values in FileTree): sequence of strings overwriting the possible values for a particular placeholder

        :param tree: Definition of pipeline input/output files
        """
        from .job import RunMethod
        templates = set.union(*[script.filter_templates(output=True, all_templates=tree.template_keys()) for script in self.scripts])
        requested_templates = getattr(
            args, 'templates', 
            None if len(self.default_output) == 0 else self.default_output
        )
        not_in_tree = [template for template in requested_templates if template not in tree.template_keys()]
        if len(not_in_tree) > 0:
            raise ValueError(f"Requested templates {not_in_tree} are not defined in the FileTree")
        unrecognised_templates = set(requested_templates).difference(templates)
        if len(unrecognised_templates) > 0:
            raise ValueError(f"Requested templates {unrecognised_templates} cannot be produced by this pipeline")
        for var in tree.placeholders:
            if isinstance(var, str) and getattr(args, var, None) is not None:
                tree.placeholders[var] = getattr(args, var)
        concrete = self.generate_jobs(tree)
        torun = concrete.filter(requested_templates, overwrite=args.overwrite, overwrite_dependencies=args.overwrite_dependencies, skip_missing=args.skip_missing)
        if not args.quiet:
            torun.report()
        if getattr(args, "batch", False):
            use_label = any(job.batch is not None for job in concrete.jobs)
            torun = torun.batch(use_label=use_label)
        if datalad is not None and args.datalad:
            torun.run_datalad()
        torun.run(RunMethod[args.pipeline_method], wait_for=() if args.job_hold == '' else args.job_hold.split(','))

    def cli(self, tree: Optional[FileTree]=None, include_vars=None, exclude_vars=(), cli_arguments=None):
        """
        Run the pipeline from the command line.

        :param tree: `file_tree.FileTree` object describing the directory structure for the input/output files (defaults to datalad tree).
        :param include_vars: if provided, only include expose variables in this list to the command line
        :param exclude_vars: exclude variables in this list from the command line
        """
        if tree is None:
            if datalad is None:
                raise ValueError("Argument 'tree' missing: please provide a FileTree describing the directory structure for the pipeline")
            from .datalad import get_tree
            try:
                tree = get_tree()
            except IOError:
                raise ValueError("Pipeline run outside of a datalad dataset, so a FileTree needs to be explicitly provided using the 'tree' argument")
            if tree is None:
                raise ValueError("No reference FileTree for pipeline found")

        parser = self.default_parser(tree=tree, include_vars=include_vars, exclude_vars=exclude_vars)
        args = parser.parse_args(cli_arguments)
        self.run_cli(args, tree)

    def move_to_subtree(self, sub_tree=None, other_mappings=None):
        """
        Create a new pipeline that runs in a sub-tree of a larger tree rather than at the top level.

        :param sub_tree: name of the sub-tree in the FileTree
        :param other_mappings: other mappings between templates or placeholder names and their new values
        """
        if other_mappings is None:
            other_mappings = {}
        all_scripts = [script.move_to_subtree(sub_tree, other_mappings) for script in self.scripts]
        new_default_submit = _update_kwargs(self.default_submit, sub_tree, other_mappings)
        return Pipeline(all_scripts, [_update_key(key, sub_tree, other_mappings) for key in self.default_output], new_default_submit)

    @classmethod
    def merge(cls, pipelines: Collection["Pipeline"]):
        """
        Combine multiple pipelines into a single one.

        :param pipelines: pipelines containing part of the jobs
        :return: parent pipeline containing all of the jobs in pipelines
        """
        new_pipeline = Pipeline()
        for pipeline in pipelines:
            new_pipeline.scripts.extend([s.copy() for s in pipeline.scripts])
            new_pipeline.default_output.extend(pipeline.default_output)
        return new_pipeline

    def find(self, function: Union[str, Callable]):
        """
        Iterate over any pipeline scripts that run the provided function.

        Either the function itself or the name of the function can be given.
        """
        for script in list(self.scripts):
            if script.function == function or getattr(script.function, '__name__', None) == function:
                yield script

    def remove(self, function: Union[str, Callable]):
        """
        Remove any pipeline scripts that run the provided function from the pipeline.

        Either the function itself or the name of the function can be given.
        """
        for script in self.find(function):
            self.scripts.remove(script)

    def configure(self, kwargs):
        """
        Override the values passed on to the keyword arguments of all the scripts.

        Any keywords not expected by a script will be silently skipped for that script.
        """
        for script in self.scripts:
            try:
                script.configure(kwargs, allow_new_keywords=False, check=False)
            except KeyError:
                pass

    def add_to_graph(self, graph: graphviz.Digraph=None, tree: FileTree=None):
        """
        Add all the pipeline functions to the provided graph.

        :param graph: GraphViz graph object (will be altered)
        :param tree: concrete FileTree
        """
        if graph is None:
            graph = graphviz.Digraph("pipeline", format="svg")
        placeholder_color = {}
        for idx, script in enumerate(self.scripts):
            script.add_node(graph, idx, tree, placeholder_color)
        return graph


class PipedFunction:
    """Represents a function stored in a pipeline."""

    def __init__(self, function, submit_params: Dict, kwargs=None, no_iter=None, override=None, as_path=True, batch=None):
        """
        Wrap a function with additional information to run it in a pipeline.

        :param function: python function that will be run in pipeline.
        :param submit_params: parameters to submit job running python function to cluster using `fsl_sub`.
        :param kwargs: maps function keyword arguments to templates, variables, or actual values.
        :param templates: maps function keyword arguments to templates in the FileTree with additional information on whether the file is input/output/reference.
        :param no_iter: which parameters to not iterate over (i.e., they are passed to the function in an array).
        :param override: dictionary overriding the placeholders set in the filetree.
        :param as_path: whether to pass on pathlib.Path objects instead of strings to the functions (default: True).
        :param batch: label used to batch multiple jobs into one when submitting to the cluster.
        """
        self.function = function
        self.submit_params = submit_params
        if override is None:
            override = {}
        self.override = override
        self.as_path = as_path
        self.batch = batch

        self.all_kwargs: Dict[str, Any] = {}
        self.configure(function.__annotations__)

        if kwargs is not None:
            self.configure(kwargs)

        if no_iter is None:
            no_iter = set()
        self.explicit_no_iter = set(no_iter)

    def copy(self, ):
        """Create a copy of this PipedFunction for pipeline merging."""
        new_script = copy(self)
        new_script.all_kwargs = dict(self.all_kwargs)
        self.explicit_no_iter = set(self.explicit_no_iter)
        return new_script

    @property
    def no_iter(self, ) -> Set[str]:
        """Sequence of placeholder names that should not be iterated over."""
        res = {key if value.key is None else value.key for key, value in self.placeholders.items() if value.no_iter}
        res.update(self.explicit_no_iter)
        return res

    def configure(self, kwargs, allow_new_keywords=True, check=True):
        """Override the values passed on to the keyword arguments of the script.

        :param kwargs: new placeholders/templates/values for keyword arguments
        :param allow_new_keywords: if set to False, don't allow new keywords
        """
        bad_keys = []
        signature = inspect.signature(self.function)
        has_kws = any(param.kind == param.VAR_KEYWORD for param in signature.parameters.values())

        if not allow_new_keywords:
            existing_kws = set(signature.parameters)
            if has_kws:
                existing_kws.update(self.all_kwargs.keys())
            if check:
                bad_keys = {key for key in kwargs.keys() if key not in signature.parameters}
                raise KeyError(f"Tried to configure {self} with keys that are not expected by the function: {bad_keys}")
        for key, value in kwargs.items():
            if not allow_new_keywords and key not in existing_kws:
                continue
            self.all_kwargs[key] = value

    @property
    def placeholders(self, ):
        """Return dictionary with placeholder values overriden for this function."""
        return {key: value for key, value in self.all_kwargs.items() if isinstance(value, PlaceHolder)}

    @property
    def templates(self, ):
        """Return dictionary with templates used as input, output, or reference for this function."""
        return {key: value for key, value in self.all_kwargs.items() if isinstance(value, Template)}

    @property
    def kwargs(self, ):
        """Return dictionary with keyword arguments that will be passed on to the function."""
        return {key: value for key, value in self.all_kwargs.items() if not any(
            isinstance(value, cls) for cls in (Template, PlaceHolder)
            )}

    def filter_templates(self, output=False, all_templates=None) -> Set[str]:
        """
        Find all input or output template keys.

        :param output: if set to True select the input rather than output templates
        :param all_templates: sequence of all possible templates (required if any Template keys use globbing)
        :return: set of input or output templates
        """
        res = set()
        for kwarg_key, template in self.templates.items():
            if ((template.input and not output) or
                (template.output and output)):
                template_key = kwarg_key if template.key is None else template.key

                # apply globbing if template key contains * or ?
                if '*' in template_key or '?' in template_key:
                    if all_templates is None:
                        raise ValueError(f"Template {template_key} uses globbing, but no template keys are not provided")
                    res.update(fnmatch.filter(all_templates, template_key))
                else:
                    res.add(template_key)
        return res

    def iter_over(self, tree: FileTree) -> Tuple[str, ...]:
        """
        Find all the placeholders that should be iterated over before calling the function.

        These are all the placeholders that affect the input templates, but are not part of `self.no_iter`.

        :param tree: set of templates with placeholder values
        :return: placeholder names to be iterated over sorted by name
        """
        tree = tree.update(**self.override)
        in_vars = self.all_placeholders(tree, False)
        in_vars_linked = {tree.placeholders.linkages.get(key, key) for key in in_vars}
        out_vars = {tree.placeholders.linkages.get(key, key) for key in self.all_placeholders(tree, True)}

        updated_no_iter = {
            tree.placeholders.linkages.get(
                tree.placeholders.find_key(key),
                tree.placeholders.find_key(key),
            ) for key in self.no_iter
        }
        all_in = in_vars_linked.union(updated_no_iter)
        if len(out_vars.difference(all_in)) > 0:
            raise ValueError(f"{self}: Output template depends on {out_vars.difference(all_in)}, which none of the input templates depend on")
        return tuple(sorted(
            {v for v in in_vars if tree.placeholders.linkages.get(v, v) not in updated_no_iter}, 
        ))
        
    def get_jobs(self, tree: FileTree, all_targets: Dict):
        """
        Get a list of all individual jobs defined by this function.

        :param tree: set of templates with placeholder values
        :param all_targets: mapping from filenames to Target objects used to match input/output filenames between jobs
        :return: sequence of jobs
        """
        from .job import SingleJob
        tree = tree.update(**self.override)
        to_iter = self.iter_over(tree)
        jobs = []
        for sub_tree in tree.iter_vars(to_iter):
            kwargs, in_fns, out_fns, optionals = _single_job_kwargs(self.all_kwargs, sub_tree, tree, all_targets, as_path=self.as_path)
            job_submit_params, _, _, _ = _single_job_kwargs(self.submit_params, sub_tree, tree, all_targets, as_path=False, is_submit_param=True)

            jobs.append(SingleJob(
                self.function,
                kwargs,
                job_submit_params,
                in_fns, out_fns, optionals,
                {name: sub_tree.placeholders[name] for name in to_iter},
                self.batch,
            ))
        return jobs
        
    def all_placeholders(self, tree: FileTree, output=False) -> Set[str]:
        """
        Identify the multi-valued placeholders affecting the input/output templates of this function.

        :param tree: set of templates with placeholder values
        :param output: if set to True returns the placeholders for the output than input templates
        :return: set of all placeholders that affect the input/output templates
        """
        res = set()
        for t in self.filter_templates(output, tree.template_keys()):
            res.update(tree.get_template(t).placeholders())
        if not output:
            for key, variable in self.placeholders.items():
                res.add(key if variable.key is None else variable.key)

        bad_keys = {key for key in res if key not in tree.placeholders}
        if len(bad_keys) > 0:
            raise ValueError(f"No value set for placeholders: {bad_keys}")

        _, only_multi = tree.placeholders.split()
        return {only_multi.find_key(key) for key in res if key in only_multi}


    def move_to_subtree(self, sub_tree=None, other_mappings=None):
        """
        Create a new wrapped function that runs in a sub-tree of a larger tree rather than at the top level.

        :param sub_tree: name of the sub-tree in the FileTree
        :param other_mappings: other mappings between templates or placeholder names and their new values
        """
        if other_mappings is None:
            other_mappings = {}
        new_script = copy(self)
        new_script.all_kwargs = _update_kwargs(self.all_kwargs, sub_tree, other_mappings)
        new_script.override = {_update_key(key, sub_tree, other_mappings): value for key, value in self.override.items()}
        new_script.submit_params = _update_kwargs(self.submit_params, sub_tree, other_mappings)
        return new_script

    def __repr__(self, ):
        """Print function name."""
        return f"PipedFunction({self.function.__name__})"

    def add_node(self, graph: graphviz.Graph, index, tree: FileTree, placeholder_color: Dict[str, str]):
        """
        Add a node representing this function for a pipeline diagram.

        :param graph: input pipeline diagram (will be altered)
        :param index: unique integer identifier to use within the graph
        """
        seaborn_colors = ['#0173b2', '#de8f05', '#029e73', '#d55e00', '#cc78bc', '#ca9161', '#fbafe4', '#949494', '#ece133', '#56b4e9']
        identifier = str(index) + self.function.__name__
        label = self.function.__name__
        if tree is not None:
            placs = self.iter_over(tree)
            if len(placs) > 0:
                for p in placs:
                    if p not in placeholder_color:
                        placeholder_color[p] = seaborn_colors[len(placeholder_color) % len(seaborn_colors)]
                plac_text = ';'.join(f'<font color="{placeholder_color[p]}">{p}</font>' for p in placs)
                label = fr"<{label}<br/>{plac_text}>"

        graph.node(identifier, label=label, color='red', shape='box')
        for output in (False, True):
            for t in self.filter_templates(output, tree.template_keys()):
                label = t
                if tree is not None:
                    all_plac = tree.get_template(t).required_placeholders() | tree.get_template(t).optional_placeholders()
                    multi_plac = sorted([p for p in all_plac if p not in tree.placeholders or not is_singular(tree.placeholders[p])])
                    for p in multi_plac:
                        if p not in placeholder_color:
                            placeholder_color[p] = seaborn_colors[len(placeholder_color) % len(seaborn_colors)]
                    multi_plac = ';'.join(f'<font color="{placeholder_color[p]}">{p}</font>' for p in multi_plac)
                    if len(multi_plac) > 0:
                        label = fr"<{t}<br/>{multi_plac}>"
                graph.node(t, label, color='blue')
                if output:
                    graph.edge(identifier, t)
                else:
                    graph.edge(t, identifier)

@dataclass
class Template(object):
    """Represents a keyword argument that will be mapped to a template path in the FileTree.
    
    :param key: template key in FileTree.
    :param input: Set to true if file should be considered as input (i.e., it should exist before the job is run).
    :param output: Set to true if file should be considered as output (i.e., it is expected to exist after the job is run).
    :param optional: Set to true if input/output file should be considered for creating the dependency graph, but still might not exist.
    """

    key: Optional[str] = None
    input: bool = False
    output: bool = False
    optional: bool = False

    def __call__(self, key=None, optional=False):
        """Override the template key and whether it is optional."""
        return Template(key, self.input, self.output, optional)

@dataclass
class PlaceHolder(object):
    """Represents a keyword argument that will be mapped to a placeholder value.
    
    :param key: placeholder key in FileTree.
    :param no_iter: if True the pipeline will not iterate over individual placeholder values, but rather run a single job with all possible placeholder values at once.
    """

    key: Optional[str] = None
    no_iter: bool = False

    def __call__(self, key=None, no_iter=None):
        """Override the Placeholder."""
        if no_iter is None:
            no_iter = self.no_iter
        return PlaceHolder(key, no_iter)


"""Use to mark keyword arguments that represent input filenames of the wrapped function.

These filenames are expected to exist before the function is run.

The actual filename is extracted from the FileTree based on the template key.
This template key will by default match the keyword argument name, but can be overriden by calling `In` (e.g., `In("other_key")`).
"""
In = Template(input=True)

"""Use to mark keyword arguments that represent output filenames of the wrapped function.

These filenames are expected to exist after the function is run.
An error is raised if they do not.

The actual filename is extracted from the FileTree based on the template key.
This template key will by default match the keyword argument name, but can be overriden by calling `In` (e.g., `In("other_key")`).
"""
Out = Template(output=True)

"""Use to mark keyword arguments that represent reference filenames of the wrapped function.

These filenames might or might not exist before or after the job is run.

The actual filename is extracted from the FileTree based on the template key.
This template key will by default match the keyword argument name, but can be overriden by calling `In` (e.g., `In("other_key")`).
"""
Ref = Template()

"""Use to mark keyword arguments that represent placeholder values in the pipeline.

Placeholder values are returned as :py:`PlaceholderValue` objects.
"""
Var = PlaceHolder()


def to_templates_dict(input_files=(), output_files=(), reference_files=()):
    """Convert a sequence of input/output/reference files into a template dictionary.

    Args:
        input_files (sequence, optional): Template keys representing input files. Defaults to ().
        output_files (sequence, optional): Template keys representing output files. Defaults to ().
        reference_files (sequence, optional): Template keys representing reference paths. Defaults to ().

    Raises:
        KeyError: If the same template key is used as more than one of the input/output/reference options

    Returns:
        dict: mapping of the keyword argument names to the Template objects
    """
    res = {}
    for files, cls in [
        (input_files, In),
        (output_files, Out),
        (reference_files, Ref),
    ]:
        for name in files:
            if isinstance(name, str):
                short_name = name.split('/')[-1]
            else:
                short_name, name = name
            if name in res:
                raise KeyError(f"Dual definition for template {name}")
            res[short_name] = cls(name)

    return res


"""
Named tuple representing a placeholder value with three fields.

:param key: string with placeholder key in pipeline.
:param index: integer with the index (or multiple integers with the indices if `no_iter` is set for this placeholder) of the placeholder values in list of all possible placeholder values.
:param value: actual placeholder value (or sequence of values if `no_iter is set for this placeholder)
"""
PlaceholderValue = namedtuple("PlaceholderValue", ["key", "index", "value"])


def _single_job_kwargs(wrapper_kwargs, single_tree: FileTree, full_tree: FileTree, all_targets, as_path=False, is_submit_param=False):
    """Create the keywords, input, and output filenames for a single job."""
    from .job import get_target
    final_dict = {}
    input_filenames = []
    output_filenames = []
    optional_filenames = []
    for kwarg_key, value in wrapper_kwargs.items():
        if isinstance(value, Template):
            key = kwarg_key if value.key is None else value.key

            use_glob = '*' in key or '?' in key
            iter_keys = fnmatch.filter(single_tree.template_keys(), key) if use_glob else [key]
            res = {}
            for proc_key in iter_keys:
                try:
                    proc_res = single_tree.get(proc_key)
                    is_xarray = False
                except KeyError:
                    proc_res = single_tree.get_mult(proc_key)
                    is_xarray = True
                if is_xarray:
                    if is_submit_param:
                        raise ValueError(f"Submit parameter {kwarg_key} is set to the template {key}, which has more than one possible value")
                    filenames = [get_target(fn, all_targets, proc_key) for fn in proc_res.data.flatten()]
                    if value.input:
                        input_filenames.extend(filenames)
                    if value.output:
                        output_filenames.extend(filenames)
                    if value.optional:
                        optional_filenames.extend(filenames)
                    proc_res = xarray.apply_ufunc(Path if as_path else str, proc_res, vectorize=True)
                else:
                    filename = get_target(proc_res, all_targets, proc_key)
                    if value.input:
                        input_filenames.append(filename)
                    if value.output:
                        output_filenames.append(filename)
                    if value.optional:
                        optional_filenames.append(filename)
                    proc_res = (Path if as_path else str)(proc_res)
                res[proc_key] = proc_res
            if not use_glob:
                res = res[key]
        elif isinstance(value, PlaceHolder):
            key = single_tree.placeholders.find_key(kwarg_key if value.key is None else value.key)
            plac_value = single_tree.placeholders[key]
            ref_values = list(full_tree.placeholders[key])

            if is_singular(plac_value):
                res = PlaceholderValue(key, ref_values.index(plac_value), plac_value)
                if is_submit_param:
                    res = res.value
            else:
                res = PlaceholderValue(key, tuple(ref_values.index(v) for v in plac_value), plac_value)
                if is_submit_param:
                    raise ValueError(f"Submit parameter {kwarg_key} is set to the placeholder {key}, which has more than one possible value")
        else:
            res = value
        final_dict[kwarg_key] = res
    return final_dict, input_filenames, output_filenames, optional_filenames


def check_submit_parameters(submit_params: Dict):
    """
    Check that the submit parameters are actually valid.
    
    Raises a ValueError if there are any submit parameters set not expected by fsl_sub.
    """
    signature = inspect.signature(submit)
    unrecognised = set(submit_params.keys()).difference(signature.parameters.keys())
    if len(unrecognised) > 0:
        raise ValueError(f"Unrecognised fsl_sub submit keywords: {unrecognised}")
    if 'jobhold' in submit_params:
        raise ValueError("Job-holds are managed by the fsl-pipe and cannot be set by the pipeline definition.")


def _update_key(key, sub_tree, other_mappings):
    """Update template key with sub_tree precursor, unless listed in other_mappings."""
    if key in other_mappings:
        return other_mappings[key]
    elif sub_tree is not None:
        return sub_tree + '/' + key
    else:
        return key


def _update_kwargs(input_dict, sub_tree, other_mappings):
    """Update placeholders and templates in input_dict with sub_tree precursor, unless listed in other_mappings."""
    kwargs = {}
    for key, value in input_dict.items():
        kwargs[key] = value
        if isinstance(value, PlaceHolder) or isinstance(value, Template):
            use_key = value.key if value.key is not None else key
            kwargs[key] = value(_update_key(use_key, sub_tree, other_mappings))
    return kwargs


pipe = Pipeline()
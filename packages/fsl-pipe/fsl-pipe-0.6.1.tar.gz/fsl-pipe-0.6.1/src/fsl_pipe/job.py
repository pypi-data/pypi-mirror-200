"""Defines pipeline interface after it has been split into individual jobs based on a FileTree."""
from functools import lru_cache
from file_tree.file_tree import FileTree
from typing import Optional, Set, Dict, Collection, Any, Callable, Sequence, List, Tuple
from enum import Enum
from fsl.utils.fslsub import func_to_cmd
from loguru import logger
from pathlib import Path
from fsl_sub import submit, config
import re
import inspect
from contextlib import contextmanager
import fnmatch
from warnings import warn

class OutputMissing(IOError):
    """Raised if a job misses the output files."""
    pass


class InputMissingRun(IOError):
    """Raised if a job misses the input files when it is being launched."""
    pass
class InputMissingPipe(IOError):
    """Raised if a job misses input files while it is being added to the pipeline."""
    def __init__(self, target, missing, dependency_graph=None):
        self.target = target
        self.missing = missing
        if dependency_graph is None:
            dependency_graph = []
        self.dependency_graph = dependency_graph
        super().__init__("")

    def __str__(self, ):
        dependency = ' -> '.join([str(d) for d in self.dependency_graph])
        return f"{self.target} can not be added to pipeline as it is missing required input files: {self.missing} (dependency_graph: {dependency} )"


class RunMethod(Enum):
    """How to run the individual jobs."""

    local = 1
    submit = 2
    dask = 3

    def default():
        """Return default RunMethod, which is `submit` on a cluster and `local` otherwise."""
        return RunMethod.submit if config.has_queues() else RunMethod.local


class JobList:
    """Pipeline with a concrete set of jobs.
    
    Produced from a :class:`fsl_pipe.pipeline.Pipeline` based on the provided `FileTree`.

    The default `JobList` produced by `Pipeline.generate_jobs` is unsorted and 
    needs to be sorted by running `filter` before running.
    """

    def __init__(self, tree: FileTree, jobs: Sequence["SingleJob"], targets: Dict[str, "FileTarget"]):
        """Create a new concrete set of jobs."""
        self.tree = tree
        self.jobs = jobs
        self.targets = targets

    def __len__(self, ):
        return len(self.jobs)

    def filter(self, templates: Collection[str], overwrite=False, overwrite_dependencies=False, skip_missing=False) -> "JobList":
        """Filter out a subset of jobs.

        This does a total of three things:
        - Only include jobs needed to create the templates or file patterns given in `templates`.
        - Exclude jobs for which output files already exist, unless requested by `overwrite` or `overwrite_dependencies`.
        - Sort the jobs, so that dependencies are run before the jobs that depend on them.

        :param templates: target template keys; Any jobs required to produce those files will be kept in the returned pipeline
        :param overwrite: if True overwrite the files matching the template even if they already exist, defaults to False
        :param overwrite_dependencies: if True rerun any dependent jobs even if the output of those jobs already exists, defaults to False
        :return: Concrete pipeline with the jobs needed to produces `templates` (with optional overriding)
        """
        def add_target(target: "FileTarget", warn_msg=""):
            if target.exists() and (not overwrite or target.producer is None):
                return
            if target.producer is None:
                warn(f"No job found that produces {target.filename} {warn_msg}")
                return
            try:
                target.producer.add_to_jobs(all_jobs, overwrite=overwrite, overwrite_dependencies=overwrite_dependencies)
            except InputMissingPipe as e:
                if skip_missing:
                    return
                e.dependency_graph.insert(0, e.target)
                e.target = target.filename
                raise

        all_jobs: Tuple[List[SingleJob], Set[SingleJob]] = ([], set())
        if templates is None:
            for target in self.targets.values():
                add_target(target)
        else:
            for template in templates:
                if template in self.tree.template_keys():
                    for filename in self.tree.get_mult(template).data.flatten():
                        target = get_target(filename, self.targets, from_template=template)
                        add_target(target, f"(part of template {template})")
                else:
                    matches = get_matching_targets(template, self.targets)
                    if len(matches) == 0:
                        warn(f"No files were found that match {template}. It is not a template in the FileTree nor does it match any files that can be produced by this pipeline.")
                    for target in matches:
                        add_target(target, f"(matches {template})")
        return JobList(self.tree, all_jobs[0], self.targets)

    def batch(self, use_label=False, only_connected=False, split_on_ram=False, use_placeholders=True):
        """Batches groups of jobs into a single job.

        Two jobs will be batched if:

            1. There are no intermediate jobs that need to run between the two and cannot be included in the same batch (because of #3 below).
            2. One of the jobs depend on the other. This is disabled by default. Enable it by setting `only_connected` to True.
            3. The jobs are similar. Jobs are similar if they match all of the (enabled) properties listed below:

                a) They have the same batch label (set during pipeline creating using the `@pipe(batch=<batch label>)`. This can be enabled by setting the `use_label` keyword to True. If enabled, jobs without a batch label will never be merged.
                b) The jobs have the same submit parameters (e.g., "architecture", "coprocessor"), except for "jobtime" and "name". "jobram" can also be ignored by setting the `split_on_ram` keyword to True.
                c) The jobs have the same placeholder values. This will prevent jobs from different subjects to be merged with each other. It can be disabled by setting the `use_placeholders` to False. Alternatively, a subset of placeholder values could be considered by passing `use_placeholders` to a sequence of placeholders to consider (e.g., `use_placeholders=["subject", "session"]` will not merge jobs with different "subject" or "session" placeholder values, but will ignore any other placeholders).
        """
        all_flags = {key for job in self.jobs for key in job.submit_params.keys()}.difference(["jobtime", "name"])
        if not split_on_ram and "jobram" in all_flags:
            all_flags.remove("jobram")
        all_flags = sorted(all_flags)

        job_labels = []
        for job in self.jobs:
            label = []
            label.append(job.batch if use_label else 1)
            label.extend(job.submit_params.get(key, None) for key in all_flags)
            if use_placeholders:
                if use_placeholders == True:
                    parameters = job.set_parameters
                else:
                    parameters = {key: value for key, value in job.set_parameters.items() if key in use_placeholders}
                label.append(frozenset(parameters.items()))
            job_labels.append(tuple(label))

    
        to_batch = {
            tb: set(job for (job, label) in zip(self.jobs, job_labels) if label == tb)
            for tb in set(job_labels)
        }
        jobs = set(self.jobs)
        for to_batch, batching in to_batch.items():
            if to_batch[0] is None:
                # do not batch jobs without a label set (if `use_label` is True)
                continue
            other_jobs = jobs.difference(batching)
            new_jobs = batch_connected_jobs(batching, other_jobs)
            if not only_connected:
                new_jobs = batch_unconnected_jobs(new_jobs, other_jobs)
            jobs = set(new_jobs).union(other_jobs)
        return JobList(self.tree, jobs, self.targets)

    def report(self):
        """Produce tree reports with the relevant input/output templates."""
        from rich import print, color, tree
        if len(self.jobs) == 0:
            print("No jobs will be run.")
            return

        all_inputs = set.union(*[set(j.input_targets) for j in self.jobs])
        all_outputs = set.union(*[set(j.output_targets) for j in self.jobs])
        templates = {
            template
            for fns in (all_inputs, all_outputs)
            for target in fns
            for template in target.from_templates
        }

        def proc_line(tree_obj):
            for t in tree_obj.children:
                proc_line(t)
            line = tree_obj.label
            start = line.index('[cyan]') + 6
            end = line.index('[/cyan]')
            key = line[start:end]
            input_count = 0
            output_count = 0
            overwrite_count = 0
            exists_count = 0

            for fn in self.tree.get_mult(key).data.flatten():
                target = get_target(fn, self.targets)
                is_output = False
                is_input = False
                if target in all_outputs:
                    is_output = True
                if target in all_inputs:
                    is_input = True
                if target.exists() and is_output:
                    overwrite_count += 1
                elif is_output:
                    output_count += 1
                elif target.exists():
                    exists_count += 1
                    if is_input:
                        input_count += 1
            if (input_count + output_count + overwrite_count) == 0:
                return
            counter = "/".join([str(number) if color is None else f"[{color}]{number}[/{color}]" 
                for number, color in [
                    (overwrite_count, 'red'),
                    (output_count, 'yellow'),
                    (input_count, 'blue'),
                ]])
            tree_obj.label = f"{line} [{counter}]"

        for rich_obj in self.tree.filter_templates(templates).fill()._generate_rich_report():
            if isinstance(rich_obj, tree.Tree):
                proc_line(rich_obj)
            print(rich_obj)

    def run_datalad(self, ):
        """Make sure we can run the pipeline.

        Calls `datalad.get` on all input files and `datalad.unlock` on all output files.
        """
        input_targets = set()
        output_targets = set()

        for job_group in self.jobs.values():
            for j in job_group:
                input_targets.update(j.exists_before)
                output_targets.update(j.exists_after)
        
        input_targets.difference_update(output_targets)
        input_fns = [t.filename for t in input_targets]
        output_fns = [t.filename for t in output_targets if t.exists]

        from .datalad import get_dataset
        ds = get_dataset()
        ds.get(input_fns)
        ds.unlock(output_fns)

    def run(self, method: RunMethod=None, wait_for=()):
        """Run all the jobs that are required to produce the given templates.

        :param method: defines how to run the job
        :param wait_for: job IDs to wait for before running pipeline
        :return: set of all the jobs that need to be run to produce the template files
        """
        if method is None:
            method = RunMethod.default()
        elif not isinstance(method, RunMethod):
            method = RunMethod[method]
        if len(self.jobs) == 0:
            logger.info("No new jobs being run/submitted")
            return

        prev_count = 0
        run_jobs: Dict[SingleJob, Any] = {}
        while len(run_jobs) < len(self.jobs):
            for job in self.jobs:
                if job in run_jobs or any(j in self.jobs and j not in run_jobs for _, j in job.dependencies(only_missing=False)):
                    continue
                dependencies = [run_jobs[j] for _, j in job.dependencies(only_missing=False) if j in run_jobs]
                if len(dependencies) == 0:
                    dependencies = wait_for
                run_jobs[job] = job(
                    method=method,
                    wait_for=dependencies,
                )
            if len(run_jobs) == prev_count:
                raise ValueError("Unable to run/submit all jobs. Are there circular dependencies?")
            prev_count = len(run_jobs)


class JobParent:
    """Parent for `SingleJob` and `BatchJob`.
    """
    input_targets: Set["FileTarget"]
    output_targets: Set["FileTarget"]
    optional_targets: Set["FileTarget"]

    #@lru_cache(None)
    def dependencies(self, only_missing=True) -> Set[Optional["SingleJob"]]:
        """Return jobs on which this job depends.

        By default it only returns those related with missing input files.

        :param only_missing: set to False to also return dependencies that produce files that already exist on disk
        """
        jobs = set()
        for target in self.input_targets:
            if not (only_missing and target.exists()):
                jobs.add((target in self.optional_targets, target.producer))
        return jobs

    def missing_output(self, reset_cache=False):
        """
        Create a list of filenames that do not exist on disk.

        Optional outputs are not considered.

        :param reset_cache: set to True to not rely on an existing cached existence check
        """
        missing = set()
        for to_check in self.output_targets:
            if to_check in self.optional_targets:
                continue
            if reset_cache:
                to_check.reset_existence()
            if not to_check.exists():
                missing.add(to_check)
        return missing

    def missing_input(self, reset_cache=False, ignore_expected=False):
        """
        Create a list of filenames that do not exist on disk.

        Optional inputs are not considered.

        :param reset_cache: set to True to not rely on an existing cached existence check
        :param ignore_expected: set to True to ignore any missing files that have a job that will produce them in the pipeline
        """
        missing = set()
        for to_check in self.input_targets:
            if to_check in self.optional_targets:
                continue
            if reset_cache:
                to_check.reset_existence()
            if ignore_expected and to_check.producer is not None:
                continue
            if not to_check.exists():
                missing.add(to_check)
        return missing

    def add_to_jobs(self, all_jobs, overwrite=False, overwrite_dependencies=False):
        """Mark this job and all of its dependencies to run.

        This job is marked to run, if any of the output does not yet exist or overwrite is True.
        The dependencies are marked to run, if this job runs and either their output does not exist or overwrite_dependencies is True.

        :param all_jobs: list of individual jobs. This job and all required jobs are added to this list.
        :param overwrite: if True mark this job even if the output already exists, defaults to False
        :param overwrite_dependencies: if True mark the dependencies of this job even if their output already exists, defaults to False
        """
        if self in all_jobs[1]:
            return
        if not overwrite and len(self.missing_output()) == 0:
            return
        missing = self.missing_input(ignore_expected=True)
        if len(missing) > 0:
            raise InputMissingPipe(self, {m.filename for m in missing})
        subjobs = ([], set(all_jobs[1]))
        for optional, job in self.dependencies(only_missing=not overwrite_dependencies):
            try:
                if job is not None:
                    job.add_to_jobs(subjobs, overwrite_dependencies, overwrite_dependencies) and not optional
            except InputMissingPipe as e:
                if optional:
                    continue
                e.dependency_graph.insert(0, e.target)
                e.target = self
                raise
        all_jobs[0].extend(subjobs[0])
        all_jobs[1].update(subjobs[0])
        all_jobs[0].append(self)
        all_jobs[1].add(self)

    def __call__(self, method: RunMethod, wait_for=()):
        """Run the job."""
        if method == RunMethod.local:
            self.prepare_run()
            missing = self.missing_input()
            if len(missing) > 0:
                raise InputMissingRun(f"{self} can not run as it misses required input files: {missing}")
            logger.info(f"running {self}")
            self.job = self.function(**self.kwargs)
            missing = self.missing_output(reset_cache=True)
            if len(missing) > 0:
                raise OutputMissing(f"{self} failed to produce required output files: {missing}")
        elif method == RunMethod.submit:
            from .pipeline import Template
            self.prepare_run()
            local_submit = dict(self.submit_params)
            if 'logdir' not in local_submit:
                local_submit['logdir'] = 'log'
            Path(local_submit['logdir']).mkdir(exist_ok=True, parents=True)
            if 'name' not in local_submit:
                local_submit['name'] = self.job_name()
            cmd = func_to_cmd(self.function, (), self.kwargs, local_submit['logdir'], clean="on_success")
            self.job = submit(cmd, jobhold=wait_for, **local_submit)
            logger.debug(f"submitted {self} with job ID {self.job}")
        elif method == RunMethod.dask:
            import dask
            def dask_job(*other_jobs):
                if any(a != 0 for a in other_jobs):
                    logger.debug(f"{self} skipped because dependencies failed")
                    return 1
                try:
                    self(RunMethod.local)
                except Exception as e:
                    logger.exception(f"{self} failed: {e}")
                    return 1
                logger.debug(f"Running {self} using dask")
            self.job = dask.delayed(dask_job, name=str(self))(wait_for)
        return self.job

    def prepare_run(self):
        """
        Prepare to run this job.

        Steps:
        1. Creates output directory
        """
        for target in self.output_targets:
            target.filename.parent.mkdir(parents=True, exist_ok=True)

class SingleJob(JobParent):
    """A single job within a larger pipeline."""

    def __init__(self, function: Callable, kwargs, submit_params, input_targets, output_targets, optionals, set_parameters=None, batch=None):
        """
        Create a single job that can be run locally or submitted.

        :param function: python function
        :param kwargs: keyword arguments
        :param submit_params: instructions to submit job to cluster using `fsl_sub`
        :param input_targets: set of all filenames expected to exist before this job runs
        :param output_targets: set of all filenames expected to exist after this job runs
        :param optionals: set of filenames that are used to generate the dependency graph and yet might not exist
        :param set_parameters: dictionary with placeholder values used to distinguish this SingleJob with all those produces for the same function
        :param batch: label used to batch multiple jobs into one when submitting to the cluster
        """
        self.function = function
        if set_parameters is None:
            set_parameters = {}
        self.set_parameters = set_parameters
        self.kwargs = kwargs
        self.input_targets = input_targets
        self.output_targets = output_targets
        self.optional_targets = set(optionals)
        self.submit_params = submit_params
        self.batch = batch
        for target in self.input_targets:
            target.required_by.add(self)
        for target in self.output_targets:
            target.producer = self

    def job_name(self, ):
        """Return a string representation of this job."""
        if len(self.set_parameters) > 0:
            parameter_string = '_'.join([f"{key}-{value}" for key, value in self.set_parameters.items()])
            name = f"{self.function.__name__}_{parameter_string}"
        else:
            name = self.function.__name__
        value = re.sub(r'[^\w\s-]', '', name).strip().lower()
        return re.sub(r'[-\s]+', '-', value)

    def __repr__(self, ):
        """Print job as a function call."""
        parameter_string = ', '.join([f"{key}={value}" for key, value in self.set_parameters.items()])
        return f"{self.function.__name__}({parameter_string})"


def get_target(filename: Path, all_targets, from_template=None) -> "FileTarget":
    """
    Return a :class:`FileTarget` matching the input `filename`.

    If the `FileTarget` for `filename` is already in `all_targets`, it will be returned.
    Otherwise a new `FileTarget` will be added to `all_targets` and returned.

    :param filename: path to the input/intermediate/output filename
    :param all_targets: dictionary of all FileTargets
    :param from_template: template key used to obtain the filename
    """
    abs_path = Path(filename).absolute()
    if abs_path not in all_targets:
        all_targets[abs_path] = FileTarget(filename)
    if from_template is not None:
        all_targets[abs_path].from_templates.add(from_template)
    return all_targets[abs_path]


def get_matching_targets(pattern: str, all_targets) -> List["FileTarget"]:
    """
    Return all :class:`FileTarget` that match the given input pattern.

    :param pattern: filename definition supporting Unix shell-style wildcards as described in https://docs.python.org/3/library/fnmatch.html
    :param all_targets: dictionary of all FileTargets
    """
    abs_pattern = str(Path(pattern).absolute())
    matches = []
    for path, target in all_targets.items():
        if fnmatch.fnmatch(str(path), abs_pattern):
            matches.append(target)
    return matches


class FileTarget:
    """Input, intermediate, or output file.

    See :func:`get_target` for instructions on creating a new `FileTarget`.

    If a specific :class:`SingleJob` produces a filename, this can be indicated by setting :attr:`producer`:

    .. code-block:: python

        get_target(filename, all_targets).producer = job

    This will raise a `ValueError` if the filename is already produced by another job.

    If a specific :class:`SingleJob` requires a filename, this can be indicated by adding it to :attr:`required_by`:

    .. code-block:: python

        get_target(filename, all_targets).required_by.add(job)

    Filename existence can be checked using :meth:`exists`.
    This method uses caching. To reset the cache run :meth:`reset_existence`.

    To check if the filename can be created by this pipeline (or already exists) run :meth:`expected`.
    """

    def __init__(self, filename: Path):
        """
        Create a new target based on the provided filename.

        Do not call this method directly. 
        Instead use :func:`get_target`.

        :param filename: filename
        """
        self.filename = Path(filename)
        self._producer = None
        self.required_by: Set[SingleJob] = set()
        self.from_templates: Set[str] = set()

    def exists(self) -> bool:
        """
        Test whether file exists on disk.

        This function is lazy; once it has been checked once it will keep returning the same result.

        To reset use :meth:`reset_existence`.
        """
        if not hasattr(self, "_exists"):
            self._exists = self.filename.is_symlink() or self.filename.exists()
        return self._exists

    def reset_existence(self, ):
        """Ensure existence is checked again when running :meth:`exists`."""
        if hasattr(self, "_exists"):
            del self._exists

    def expected(self, ):
        """
        Return whether the file can be produced by the pipeline (or already exists).

        Returns False if the file does not exist and there is no way to produce it. Otherwise, True is returned
        """
        if self.exists():
            return True
        if self.producer is None:
            return False
        return self.producer.expected()

    @property
    def producer(self, ) -> SingleJob:
        """Job that can produce this file."""
        return self._producer

    @producer.setter
    def producer(self, new_value):
        if self._producer is not None:
            if self._producer is new_value:
                return
            raise ValueError(f"{self} can be produced by both {self.producer} and {new_value}")
        self._producer = new_value

    def __repr__(self, ):
        """Print filename of target."""
        return f"FileTarget({str(self.filename)})"


@contextmanager
def update_closure(*dictionaries, **kwargs):
    """Add the provided dictionaries to the globals dictionary.

    Inside the `with` block all the dictionary keys will be available in the local environment.
    After the `with` block ends the local environment will be cleaned up again.
    
    Use like this:

    .. code-block:: python

        def my_func()
            with add_to_globals({'a': 3}):
                print(a)  # prints 3
            print(a)  # raises a NameError (or prints whatever `a` is set to in the global environment)
    """
    func_globals = inspect.stack()[2].frame.f_globals

    # merge input dictionaries
    new_kwargs = {}
    for d in dictionaries:
        new_kwargs.update(d)
    new_kwargs.update(kwargs)

    to_restore = {}
    to_delete = set()
    for key in new_kwargs:
        if key in func_globals:
            to_restore[key] = func_globals[key]
        else:
            to_delete.add(key)

    func_globals.update(new_kwargs)
    yield  # return to run the code within the with-block

    # clean up the environment
    func_globals.update(to_restore)
    for key in to_delete:
        del func_globals[key]
    del func_globals


def call_batched_jobs(funcs, kwargs):
    for f, k in zip(funcs, kwargs):
        f(**k)

class BatchJob(JobParent):
    """Batched combination of multiple `SingleJob` instances that will be submitted together.
    """
    function = staticmethod(call_batched_jobs)

    def __init__(self, *sub_jobs):
        """Creates a new `BatchJob` from sub_jobs.

        `sub_jobs` can be either `SingleJob` or `BatchJob`. In either case they will be run in the order in which they are supplied.
        """
        self.torun: Sequence[SingleJob] = []
        for job in sub_jobs:
            if isinstance(job, BatchJob):
                self.torun.extend(job.torun)
            else:
                assert isinstance(job, SingleJob)
                self.torun.append(job)
        self.torun_set = set(self.torun)

        self.output_targets = {t for job in self.torun for t in job.output_targets}
        for t in self.output_targets:
            t._producer = self
        self.input_targets = {t for job in self.torun for t in job.input_targets if t not in self.output_targets}
        for t in self.input_targets:
            t.required_by.add(self)

        self.optional_targets = set.union(
            {
                t for t in self.output_targets
                if not any(t in job.output_targets and t not in job.optional_targets for job in self.torun)
            },
            {
                t for t in self.input_targets
                if not any(t in job.input_targets and t not in job.optional_targets for job in self.torun)
            },
        )

        as_tuples = set.intersection(*[{(key, value) for key, value in job.set_parameters.items()} for job in self.torun])
        self.set_parameters = {key: value for key, value in as_tuples}

    @property
    def batch(self, ):
        b = self.torun[0].batch
        if all(job.batch is not None and job.batch == b for job in self.torun):
            return b
        return None

    @property
    def kwargs(self, ):
        return {
            'funcs': [job.function for job in self.torun],
            'kwargs': [job.kwargs for job in self.torun],
        }

    @property
    def submit_params(self, ):
        def sum_value(name, *times):
            total = sum(int(t) for t in times if t is not None)
            return None if total == 0 else total

        def max_value(name, *rams):
            if any(r is not None for r in rams):
                return max(int(r) for r in rams if r is not None)
            return None

        def extend(name, *vars):
            all_vars = set()
            for v in vars:
                if v is not None:
                    all_vars.update(v)
            return list(all_vars)

        def unique_param(name, *flags):
            not_none = {f for f in flags if f is not None}
            if len(not_none) == 0:
                return None
            elif len(not_none) == 1:
                return not_none.pop()
            else:
                raise ValueError(f"Multiple different values for submit parameter flag {name} found. fsl-pipe does not know which one to choose out of: {not_none}")

        to_combine = {
            'jobtime': sum_value,
            'jobram': max_value,
            'threads': max_value,
            'export_vars': extend,
        }

        all_flags = {flag for job in self.torun for flag in job.submit_params.keys()}
        return {
            flag: to_combine.get(flag, unique_param)(flag, *[job.submit_params.get(flag, None) for job in self.torun])
            for flag in all_flags
        }

    def job_name(self, ):
        """Return a string representation of this job."""
        base = "" if self.batch is None else self.batch + '_'
        func_name = "-".join(sorted({job.function.__name__ for job in self.torun}))
        if len(self.set_parameters) > 0:
            parameter_string = '_'.join([f"{key}-{value}" for key, value in self.set_parameters.items()])
            name = f"{func_name}_{parameter_string}"
        else:
            name = func_name
        value = re.sub(r'[^\w\s-]', '', name).strip().lower()
        return base + re.sub(r'[-\s]+', '-', value)

    def __repr__(self, ):
        """Print job as a function call."""
        return f"Batch({self.torun})"


def has_dependencies(possible_parent: JobParent, possible_children: Set[JobParent], all_jobs):
    if possible_parent in possible_children:
        return True
    for _, child in possible_parent.dependencies(only_missing=False):
        if child in all_jobs and has_dependencies(child, possible_children, all_jobs):
            return True
    return False


def batch_connected_jobs(to_batch: Sequence[SingleJob], other_jobs: Collection[SingleJob]) -> List[JobParent]:
    """Iteratively combines two jobs 

    Two jobs will be batched if:
    1. They are both in `to_batch`
    2. One of the jobs depends on the other
    3. There is no other job that needs to run between these two jobs.
    Iteration through the jobs will continue until no further batching is possible.
    """
    other_jobs = set(other_jobs)
    batches = set(to_batch)
    nbatches_prev = len(batches) * 2
    while len(batches) != nbatches_prev:
        nbatches_prev = len(batches)
        for job in set(batches):
            if job not in batches:
                continue
            for _, dependency in job.dependencies(only_missing=False):
                if job in batches and dependency in batches:
                    # properties 1 and 2 are met; now checking property 3
                    all_jobs = set.union(batches, other_jobs)
                    indirect_dependency = any(has_dependencies(d, {dependency}, all_jobs) for _, d in job.dependencies(only_missing=False) if d in all_jobs and d != dependency)
                    if not indirect_dependency:
                        batches.remove(job)
                        batches.remove(dependency)
                        batches.add(BatchJob(dependency, job))
                        break
    return list(batches)


def batch_unconnected_jobs(to_batch: Sequence[JobParent], other_jobs: Collection[JobParent]) -> List[BatchJob]:
    """Batch jobs into generational sets

    All jobs that do not depend on any other job in `to_batch` will be added to the first generational batch.
    All jobs that only depend on the first generational batch will be added to the second.
    And so forth, until all jobs have been added to a generation.

    Only dependencies through `other_jobs` will be considered.
    """
    to_batch = set(to_batch)
    all_jobs = set.union(to_batch, other_jobs)

    generations = []

    while len(to_batch) > 0:
        generations.append(set())
        for job in to_batch:
            if not any(has_dependencies(dependency, to_batch, all_jobs) for _, dependency in job.dependencies(only_missing=False) if dependency in all_jobs):
                generations[-1].add(job)
        to_batch.difference_update(generations[-1])
    return [jobs.pop() if len(jobs) == 1 else BatchJob(*jobs) for jobs in generations]



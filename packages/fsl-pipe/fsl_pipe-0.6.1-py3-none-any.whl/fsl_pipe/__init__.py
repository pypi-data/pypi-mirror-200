"""
Declarative pipeline definition based on filetrees.

Typical usage:

.. code-block:: python

    from fsl_pipe import pipe, In, Out, Ref, Var

    @pipe
    def job(input_file: In, output_file: Out):
        # code to convert `input_file` to `output_file`

    pipe.cli()  # runs command line interface
"""
from .pipeline import Pipeline, pipe, In, Out, Ref, Var
from .job import update_closure
__version__ = '0.6.1'
"""A simple StepImplementer that prints out a greeting. See the HelloShell example for an upgraded version
that runs a shell command to print the greeting.

You can run this example from the command line by creating a file named psr.yaml with these contents:

```
step-runner-config:

  examples:
    - implementer: HelloWorld
      config:
        greeting-name: Folks
```

And then running the command `psr -s examples -c psr.yaml`

Step Configuration
------------------
Step configuration expected as input to this step.
Could come from:

  * static configuration
  * runtime configuration
  * previous step results

Configuration Key             | Required? | Default                  | Description
------------------------------|-----------|--------------------------|-----------
`greeting-name`               | No        | `World`                  | Name to use in greeting message.

Result Artifacts
----------------
Results artifacts output by this step.

Result Artifact Key    | Description
-----------------------|------------
`greeting`             | Message that was printed
"""  # pylint: disable=line-too-long

from ploigos_step_runner.results import StepResult
from ploigos_step_runner.step_implementer import StepImplementer


class HelloWorld(StepImplementer):
    """
    Example StepImplementer that prints a message and does nothing else.
    """

    # Overridden to specify default values for this StepImplementer's configuration.
    @staticmethod
    def step_implementer_config_defaults():
        return {
            'greeting-name': 'World'
        }

    # Overridden to specify required configuration values. These can be specified in
    # the configuration file or calculated by previous steps in the workflow.
    @staticmethod
    def _required_config_or_result_keys():
        return []  # No required values without defaults

    # Overridden to implement the behavior of this StepImplementer.
    def _run_step(self):
        """Runs the step implemented by this StepImplementer.

        Returns
        -------
        StepResult
            Object containing the dictionary results of this step.
        """

        # Read the configuration, usually from `psr.yaml`.
        step_result = StepResult.from_step_implementer(self)
        greeting = self.get_value('greeting-name')  # Read from configuration

        # Do the actual work of the step.
        message = f"Hello {greeting}!"
        print(message)

        # Save the result. Future steps like the report step can access artifacts.
        step_result.add_artifact(
            name='greeting-output',
            value=message
        )

        return step_result

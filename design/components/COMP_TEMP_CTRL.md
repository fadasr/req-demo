# Temperature Controller Module

<!-- Sphinx-Needs component COMP_TEMP_CTRL from coffee-machine/architecture:116; source https://github.com/useblocks/sphinx-needs-demo@3c602bfedf710d2304d22a93049d7233bba93285#COMP_TEMP_CTRL. -->

Module responsible for PID-based temperature control. Interfaces: - Input: Temperature sensor (ADC) - Output: Heating element PWM control - Safety: Reports temperature status to Safety Monitor - Safety: Responds to emergency shutdown commands

## Satisfies

<!-- req-satisfies: REQ-0116 -->

"""Custom exception definition for server mlflow manager graph."""


class InvalidActionType(Exception):
    """Define InvalidActionType exception."""

    def __init__(self, passed_action_type):
        self.passed_action_type = passed_action_type
        self.message = (
            'Passed action_type "{passed_action_type}" is invalid,'
            "must be Enum value from ML_management.models.action_type.ActionType".format(passed_action_type=passed_action_type)
        )

        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (InvalidActionType, (self.passed_action_type,))


class InvalidModelName(Exception):
    """Define InvalidModelName exception."""

    def __init__(self, passed_name, kwarg):
        self.passed_name = passed_name
        self.kwarg = kwarg
        self.message = 'Passed "{kwarg}" argument value "{passed_name}" is invalid, as this model is not registered in mlflow.'.format(
            kwarg=kwarg,
            passed_name=passed_name,
        )

        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (InvalidModelName, (self.passed_name, self.kwarg))


class InvalidModelVersion(Exception):
    """Define InvalidModelVersion exception."""

    def __init__(self, passed_name, passed_version, name_kwarg, version_kwarg):
        self.passed_version = passed_version
        self.passed_name = passed_name
        self.name_kwarg = name_kwarg
        self.version_kwarg = version_kwarg
        self.message = 'Passed "{version_kwarg}" argument value "{passed_version}" is invalid, \
            as model "{passed_name}" (passed as "{name_kwarg}" argument value) has no such version.'.format(
            passed_name=passed_name,
            passed_version=passed_version,
            name_kwarg=name_kwarg,
            version_kwarg=version_kwarg,
        )

        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (
            InvalidModelVersion,
            (
                self.passed_name,
                self.passed_version,
                self.name_kwarg,
                self.version_kwarg,
            ),
        )


class KwargNotPassedWithAction(Exception):
    """Define KwargNotPassedWithAction exception."""

    def __init__(self, kwarg, passed_action_type):
        self.passed_action_type = passed_action_type
        self.kwarg = kwarg
        self.message = 'Argument "{kwarg}" cannot be ommitted with action type ActionType.{passed_action_type}.'.format(
            kwarg=kwarg,
            passed_action_type=passed_action_type,
        )

        super().__init__(self.message)

    def __reduce__(self):
        """Define reduce method to make exception picklable."""
        return (KwargNotPassedWithAction, (self.kwarg, self.passed_action_type))

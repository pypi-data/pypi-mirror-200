import os
import Ice
from askap.parset import ParameterSet

ice_path = os.path.dirname(os.path.abspath(__file__))
ice_path_schedblock = os.path.join(ice_path, 'SchedulingBlockService.ice')

Ice.loadSlice('-I{} --all {}'.format(ice_path, ice_path_schedblock))
# noinspection PyUnresolvedReferences,PyPep8Naming,PyPep8Naming
import askap.interfaces.schedblock as SB  # noqa


class SchedulingBlock(object):
    """Tool for reading infromation from the ASKAP Scheduling Block Service via ICE"""

    def __init__(self, sbid):
        """Create a SchedulingBlock object"""

        # default ice configuration
        host = 'icehost-mro.atnf.csiro.au'
        port = 4061
        timeout_ms = 5000
        default_loc = "IceGrid/Locator:tcp -h " + host + " -p " + str(port) + " -t " + str(timeout_ms)

        init = Ice.InitializationData()
        init.properties = Ice.createProperties()
        if "ICE_CONFIG" not in os.environ:
            loc = default_loc
        else:
            ice_cfg_file = os.environ['ICE_CONFIG']
            ice_parset = ParameterSet(ice_cfg_file)
            loc = ice_parset.get_value('Ice.Default.Locator', default_loc)

        init.properties.setProperty('Ice.Default.Locator', loc)
        self._communicator = Ice.initialize(init)
        self._service = SB.ISchedulingBlockServicePrx.checkedCast(
            self._communicator.stringToProxy("SchedulingBlockService@DataServiceAdapter"))
        self.id = sbid
        self.alias = self._service.getAlias(self.id)
        self.template = self._service.getSBTemplate(self.id)
        self._parameters = None

    def __del__(self):
        self._communicator.destroy()

    def get_variables(self):
        """
        :return: dynamic scheduling block variables
        :rtype: dict
        """
        return self._service.getObsVariables(self.id, "")

    def get_parameters(self):
        """
        :return: static scheduling block parameters
        :rtype: dict
        """
        self._parameters = self._service.getObsParameters(self.id)
        return self._parameters

    def get_footprint_name(self):
        """
        :return: footprint name
        :rtype: str
        """
        if self._parameters is None:
            self.get_parameters()

        fp_name_key = self.find_unique_key('footprint.name')

        return self._parameters[fp_name_key]

    def get_footprint_pitch(self):
        """
        :return: footprint pitch
        :rtype: float
        """
        if self._parameters is None:
            self.get_parameters()

        fp_name_key = self.find_unique_key('footprint.pitch')

        return float(self._parameters[fp_name_key])

    def get_footprint_rotation(self):
        """
        :return: footprint rotation
        :rtype: float
        """
        if self._parameters is None:
            self.get_parameters()

        fp_name_key = self.find_unique_key('footprint.rotation')

        return float(self._parameters[fp_name_key])

    def get_weights_prefix(self):
        """
        :return: beam weights prefix
        :rtype: str
        """
        if self._parameters is None:
            self.get_parameters()

        fp_name_key = self.find_unique_key('beam_weights')

        return self._parameters[fp_name_key]

    def find_unique_key(self, partial_key):
        """
        Find unique parameter key matching partial string. The lookup partial_key target
        is expected to be at the end of the parset key being evaluated.
        Fails if more than one key name matches partial_key.

        :param str partial_key: partial key name
        :return: full key name
        :rtype: str
        """
        fp_name_keys = [k for k in self._parameters.keys() if k.endswith(partial_key)]
        if len(fp_name_keys) == 1:
            fp_name_key = fp_name_keys[0]
        else:
            raise ValueError('Expected a single {} key, got {}'.format(partial_key, fp_name_keys))
        return fp_name_key

    def list_schedblocks(self, status="ACTIVE"):
        # noinspection PyProtectedMember
        valid_states = [str(v) for v in SB.ObsState._enumerators.values()]
        states = []
        if status == "ACTIVE":
            for st in valid_states:
                if st in ["RETIRED", "COMPLETED"]:
                    continue
                state = getattr(SB.ObsState, st)
                states.append(state)
        else:
            states = [getattr(SB.ObsState, status.upper())]
        sbids = sorted(self._service.getByState(states, ''))
        return sbids
        # return self._service.getMany(sbids)

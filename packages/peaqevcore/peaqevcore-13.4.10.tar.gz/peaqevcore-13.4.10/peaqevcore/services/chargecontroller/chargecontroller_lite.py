# from ...models.chargecontroller_states import ChargeControllerStates
# from .chargecontrollerbase import ChargeControllerBase


# class ChargeControllerLite(ChargeControllerBase):
#     def __init__(self, hub):
#         super().__init__(hub)

#     def _get_status_charging(self) -> ChargeControllerStates:
#         if self._hub.totalhourlyenergy.value >= self._hub.current_peak_dynamic and self._hub.locale.data.free_charge(self._hub.locale.data) is False:
#             ret = ChargeControllerStates.Stop
#         else:
#             ret = ChargeControllerStates.Start
#         return ret

#     def _get_status_connected(self, charger_state = None) -> ChargeControllerStates:
#         if charger_state is not None and self._hub.sensors.carpowersensor.value < 1 and self._is_done(charger_state):
#             ret = ChargeControllerStates.Done
#         else:
#             if (self._hub.totalhourlyenergy.value < self._hub.current_peak_dynamic) or self._hub.locale.data.free_charge(self._hub.locale.data) is True:
#                 ret = ChargeControllerStates.Start
#             else:
#                 ret = ChargeControllerStates.Stop
#         return ret

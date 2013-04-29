from eusful.data import EasyObject, Atom, Sequence, Dictionary

class Device(EasyObject):
  id = Atom
  name = Atom
  scale = Atom
  temperature = Atom
  target_temperature_low = Atom
  target_temperature_high = Atom
  system_mode = Atom
  heater_on = Atom
  ac_on = Atom
  fan_mode = Atom
  fan_on = Atom

class Structure(EasyObject):
  id = Atom
  name = Atom
  location = Atom
  away = Atom
  num_thermostats = Atom
  devices = Dictionary

class Account(EasyObject):
  id = Atom
  name = Atom
  structures = Dictionary

def clean_id(prepended_str):
  period = prepended_str.find('.')
  return prepended_str[period+1:]


#top level keys:
#[u'user_alert_dialog', u'schedule', u'track', u'user', u'user_settings', u'link',
#u'message_center', u'device', u'shared', u'structure', u'metadata']

#device keys:
#[u'heat_pump_comp_threshold', u'backplate_model', u'lower_safety_temp_enabled',
#u'postal_code', u'learning_mode', u'country_code', u'heat_x3_source',
#u'backplate_serial_number', u'hvac_wires', u'humidifier_type', u'dual_fuel_breakpoint_override',
#u'has_x3_heat', u'alt_heat_x2_delivery', u'device_locale', u'learning_time',
#u'has_fan', u'pin_rh_description', u'has_x2_alt_heat', u'leaf_away_high', u'heat_x2_source',
#u'aux_heat_source', u'equipment_type', u'forced_air', u'aux_lockout_leaf', u'humidifier_state',
#u'error_code', u'switch_system_off', u'has_x2_cool', u'serial_number', u'hvac_pins',
#u'creation_time', u'heat_pump_comp_threshold_enabled', u'pin_star_description',
#u'temperature_lock', u'learning_days_completed_cool', u'away_temperature_low_enabled',
#u'note_codes', u'leaf_threshold_heat', u'leaf', u'backplate_mono_info', u'alt_heat_x2_source',
#u'has_humidifier', u'leaf_type', u'current_schedule_mode', u'backplate_bsl_info',
#u'fan_cooling_readiness', u'battery_level', u'schedule_learning_reset', u'pin_y2_description',
#u'emer_heat_source', u'filter_reminder_enabled', u'compressor_lockout_leaf', u'$version',
#u'aux_heat_delivery', u'away_temperature_high', u'learning_days_completed_range',
#u'target_humidity_enabled', u'leaf_threshold_cool', u'has_dual_fuel',
#u'heatpump_setback_active', u'has_heat_pump', u'model_version', u'has_aux_heat',
#u'current_version', u'away_temperature_high_enabled', u'alt_heat_delivery', u'current_humidity',
#u'target_humidity', u'upper_safety_temp', u'heater_delivery', u'preconditioning_ready',
#u'backplate_mono_version', u'mac_address', u'cooling_source', u'type', u'lower_safety_temp',
#u'emer_heat_delivery', u'fan_mode', u'fan_cooling_enabled', u'range_enable', u'heatpump_savings',
#u'radiant_control_enabled', u'temperature_lock_low_temp', u'pin_ob_description', u'auto_away_reset',
#u'heatpump_ready', u'preconditioning_enabled', u'target_time_confidence', u'local_ip',
#u'pin_w1_description', u'cooling_x2_source', u'temperature_lock_high_temp',
#u'heat_pump_aux_threshold', u'rssi', u'has_emer_heat', u'has_alt_heat', u'leaf_schedule_delta',
#u'backplate_bsl_version', u'user_brightness', u'preconditioning_active', u'pin_w2aux_description',
#u'pin_rc_description', u'has_dehumidifier', u'leaf_learning', u'pin_y1_description',
#u'capability_level', u'available_locales', u'dehumidifier_state', u'dehumidifier_type',
#u'nlclient_state', u'upper_safety_temp_enabled', u'learning_state', u'time_to_target_training',
#u'fan_cooling_state', u'alt_heat_source', u'$timestamp', u'temperature_lock_pin_hash',
#u'heat_pump_aux_threshold_enabled', u'leaf_away_low', u'heat_x3_delivery', u'ob_orientation',
#u'temperature_scale', u'emer_heat_enable', u'time_to_target', u'auto_away_enable',
#u'pin_g_description', u'click_sound', u'has_x2_heat', u'away_temperature_low', u'heat_x2_delivery',
#u'learning_days_completed_heat', u'dual_fuel_breakpoint', u'heater_source', u'pin_c_description']

#structure keys:
#[u'num_thermostats', u'away_timestamp', u'name', u'away', u'creation_time', u'devices',
#u'renovation_date', u'postal_code', u'location', u'country_code', u'$version', u'house_type',
#u'away_setter', u'$timestamp', u'user']

#shared keys:
#[u'hvac_ac_state', u'compressor_lockout_timeout', u'hvac_alt_heat_x2_state', u'compressor_lockout_enabled',
#u'target_temperature', u'auto_away', u'can_heat', u'hvac_aux_heater_state', u'target_change_pending',
#u'hvac_heat_x2_state', u'target_temperature_low', u'target_temperature_high', u'hvac_heat_x3_state',
#u'hvac_cool_x2_state', u'$timestamp', u'hvac_heater_state', u'auto_away_learning',
#u'target_temperature_type', u'$version', u'name', u'can_cool', u'hvac_fan_state', u'current_temperature',
#u'hvac_emer_heat_state', u'hvac_alt_heat_state']

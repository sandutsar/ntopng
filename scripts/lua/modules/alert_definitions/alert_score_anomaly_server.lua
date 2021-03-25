--
-- (C) 2019-21 - ntop.org
--

-- ##############################################

local alert_keys = require "alert_keys"
local classes = require "classes"
local alert = require "alert"

-- ##############################################

local alert_score_anomaly_server = classes.class(alert)

-- ##############################################

alert_score_anomaly_server.meta = {
   alert_key = alert_keys.ntopng.alert_score_anomaly_server,
   i18n_title = "alerts_dashboard.unexpected_host_behaviour_score_server_title",
   icon = "fas fa-exclamation",
}

-- ##############################################

-- @brief Prepare an alert table used to generate the alert
-- @param value       The value got from the measurement
-- @param prediction  The value instead predicted
-- @param lower_bound The lower bound of the measurement
-- @param upper_bound The upper bound of the measurement
-- @return A table with the alert built
function alert_score_anomaly_server:init(value, prediction, upper_bound, lower_bound)
   -- Call the parent constructor
   self.super:init()

   self.alert_type_params = {
      value = value,
      prediction = prediction,
      upper_bound = upper_bound,
      lower_bound = lower_bound,
   }
end

-- #######################################################

-- @brief Format an alert into a human-readable string
-- @param ifid The integer interface id of the generated alert
-- @param alert The alert description table, including alert data such as the generating entity, timestamp, granularity, type
-- @param alert_type_params Table `alert_type_params` as built in the `:init` method
-- @return A human-readable string
function alert_score_anomaly_server.format(ifid, alert, alert_type_params)
   local alert_consts = require("alert_consts")
   
   return(i18n("alerts_dashboard.unexpected_host_behavior_description",
		{
		   host = firstToUpper(alert_consts.formatAlertEntity(ifid, alert_consts.alertEntityRaw(alert["alert_entity"]), alert["alert_entity_val"])),
		   type_of_behaviour = i18n("alert.anomalies.score_as_server") or "",
		   value = alert_type_params.value,
		   prediction = alert_type_params.prediction or 0,
		   lower_bound = alert_type_params.lower_bound or 0,
		   upper_bound = alert_type_params.upper_bound or 0,
		}))
end

-- #######################################################

return alert_score_anomaly_server

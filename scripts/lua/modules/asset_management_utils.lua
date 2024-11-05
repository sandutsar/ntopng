--
-- (C) 2024 - ntop.org
--
local dirs = ntop.getDirs()
package.path = dirs.installdir .. "/scripts/lua/modules/?.lua;" .. package.path

require "ntop_utils"
require "check_redis_prefs"
local os_utils = require "os_utils"

-- ##############################################

local asset_management_utils = {}
local table_name = "asset_management"

-- ##############################################

-- @brief insert assetkey
function asset_management_utils.insert_host(entry)


    local insert_host = ""
    
    if hasClickHouseSupport() then
        insert_host = string.format(
            "INSERT INTO %s " ..
            "(type, key, ip, mac, vlan, network, name, device_type, manufacturer, first_seen, last_seen) " ..
            "SELECT '%s','%s','%s','%s', %u, %u, %s, %u, %s, %u "..
            "WHERE NOT EXISTS ( SELECT 1 FROM %s WHERE key = '%s' )",
            table_name, 
            entry["type"],
            entry["key"],
            entry["ip"],
            entry["mac"],
            entry["vlan"],
            entry["network"],
            ternary(not isEmptyString(entry["name"]),string.format("'%s'",entry["name"]),"NULL"),
            entry["device_type"],
            ternary(not isEmptyString(entry["manufacturer"]),string.format("'%s'",entry["manufacturer"]), "NULL"),
            entry["first_seen"],
            entry["last_seen"],
            table_name,
            entry["key"]
        )
        local update_host = string.format("ALTER TABLE `%s` UPDATE `last_seen` = %u WHERE `key` == '%s'",
            table_name,
            entry["last_seen"],
            entry["key"]
        )
        --tprint(insert_host)
        interface.alert_store_query(insert_host)
        return interface.alert_store_query(update_host)
    else
        insert_host = string.format(
            "INSERT INTO %s " ..
            "(type, key, ip, mac, vlan, network, name, device_type, manufacturer, first_seen, last_seen) " ..
            "VALUES ('%s','%s','%s','%s', %u, %u, %s, %u, %s, %u, %u) "..
            "ON CONFLICT(key) DO UPDATE SET last_seen = %u;",
            table_name, 
            entry["type"],
            entry["key"],
            entry["ip"],
            entry["mac"],
            entry["vlan"],
            entry["network"],
            ternary(not isEmptyString(entry["name"]),string.format("'%s'",entry["name"]),"NULL"),
            entry["device_type"],
            ternary(not isEmptyString(entry["manufacturer"]),string.format("'%s'",entry["manufacturer"]), "NULL"),
            entry["first_seen"],
            entry["last_seen"],
            entry["last_seen"]
        )
        return interface.alert_store_query(insert_host)
    end

    -- traceError(TRACE_NORMAL, TRACE_CONSOLE, insert_host)
end

function asset_management_utils.insert_mac(entry)
    if hasClickHouseSupport() then
        local insert_mac = string.format(
            "INSERT INTO %s " ..
            "(type, key, mac, device_type, first_seen, last_seen) " ..
            "SELECT '%s','%s','%s','%s', %u, %u "..
            "WHERE NOT EXISTS ( SELECT 1 FROM %s WHERE key = '%s' )",
            table_name, 
            entry["type"],
            entry["mac"],
            entry["mac"],
            entry["device_type"],
            entry["first_seen"],
            entry["last_seen"],
            table_name,
            entry["mac"]
        )
        local update_mac = string.format("ALTER TABLE `%s` UPDATE `last_seen` = %u WHERE `key` == '%s'",
            table_name,
            entry["last_seen"],
            entry["mac"]
        )
        --tprint(insert_mac)
        interface.alert_store_query(insert_mac)
        return interface.alert_store_query(update_mac)
    else
        local insert_mac = string.format(
            "INSERT INTO %s " ..
            "(type, key, mac, device_type, first_seen, last_seen) " ..
            "VALUES ('%s','%s','%s','%s', %u, %u) "..
            "ON CONFLICT(key) DO UPDATE SET last_seen = %u ;",
            table_name, 
            entry["type"],
            entry["mac"],
            entry["mac"],
            entry["device_type"],
            entry["first_seen"],
            entry["last_seen"],
            entry["last_seen"]
        )
        return interface.alert_store_query(insert_mac)
    end
    -- traceError(TRACE_NORMAL, TRACE_CONSOLE, insert_mac)

end

-- ##############################################

return asset_management_utils

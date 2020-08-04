--
-- (C) 2019-20 - ntop.org
--
local dirs = ntop.getDirs()
package.path = dirs.installdir .. "/scripts/lua/modules/?.lua;" .. package.path

require "lua_utils"

local page_utils = require("page_utils")
local template = require "template_utils"
local json = require "dkjson"
local plugins_utils = require("plugins_utils")
local menu_alert_notifications = require("menu_alert_notifications")
local notification_configs = require("notification_configs")
local endpoints = notification_configs.get_configs()

if not haveAdminPrivileges() then
    return
end

sendHTTPContentTypeHeader('text/html')

page_utils.set_active_menu_entry(page_utils.menu_entries.endpoint_recipients)

-- append the menu above the page
dofile(dirs.installdir .. "/scripts/lua/inc/menu.lua")
-- print a notification container used by the AJAX operations
menu_alert_notifications.render_notifications('recipients', {})

page_utils.print_page_title(i18n("endpoint_notifications.recipient_list"))

-- localize endpoint name types in a table
local endpoints_types = notification_configs.get_types()
local endpoint_types_labels = {}
for endpoint_key, _ in pairs(endpoints_types) do
    endpoint_types_labels[endpoint_key] = i18n('endpoint_notifications.types.'..endpoint_key)
end

-- Prepare the response
local context = {
    notifications = {
        endpoints = endpoints_types,
        endpoint_types_labels = endpoint_types_labels,
        endpoint_list = endpoints,
    },
    template_utils = template,
    page_utils = page_utils,
    json = json,
    info = ntop.getInfo()
}

-- print config_list.html template
print(template.gen("pages/recipients_endpoint.template", context))

-- append the menu below the page
dofile(dirs.installdir .. "/scripts/lua/inc/footer.lua")

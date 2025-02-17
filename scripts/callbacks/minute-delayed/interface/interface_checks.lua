--
-- (C) 2019-24 - ntop.org
--

local dirs = ntop.getDirs()
package.path = dirs.installdir .. "/scripts/lua/modules/?.lua;" .. package.path

local checks = require "checks"

-- #################################################################
-- Just like for local_network_checks.lua, here periodic interface 
-- checks are executed with the right granularity
-- #################################################################

local checks_var = {
   ifid = nil,
   available_modules = nil,
   iface_config = nil, 
   configset = nil,
}

local granularity = "min"
local do_trace = false

-- #################################################################

checks.interfaceChecks(granularity, checks_var, do_trace)
checks.hostChecks(granularity, checks_var, do_trace)

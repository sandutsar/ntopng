<template>
    <div class="m-2 mb-3">
        <TableWithConfig ref="table_redis_stats" :table_id="table_id" :csrf="props.context.csrf"
            :f_map_columns="map_table_def_columns" :f_sort_rows="columns_sorting" @custom_event="on_table_custom_event">
        </TableWithConfig>
    </div>
</template>


<script setup>
import { ref } from "vue";
import { default as sortingFunctions } from "../utilities/sorting-utils.js";
import { default as TableWithConfig } from "./table-with-config.vue";
import formatterUtils from "../utilities/formatter-utils";
import NtopUtils from "../utilities/ntop-utils.js";

const _i18n = (t) => i18n(t);

const props = defineProps({
    context: Object,
});

const table_id = ref('redis_stats');
const table_redis_stats = ref(null);

const map_table_def_columns = (columns) => {

    let map_columns = {
        "command": (value, row) => {
            return value.name
        },
        "hits": (value, row) => {
            return value
        },
    };

    columns.forEach((c) => {
        c.render_func = map_columns[c.data_field];
        if (c.id === "actions") {
            const visible_dict = {
                timeseries: props.context.timeseries_available,
            };
            c.button_def_array.forEach((b) => {
                if (!visible_dict[b.id]) {
                    b.class.push("disabled");
                }
            });
        }
    });

    return columns;
};

/* ************************************** */

// This function handles the sorting of the columns
function columns_sorting(col, r0, r1) {
    if (col != null) {
        if (col.id == "command") {
            return sortingFunctions.sortByName(r0.command.name, r1.command.name, col.sort);
        } else if (col.id == "hits") {
            return sortingFunctions.sortByNumber(r0.hits, r1.hits, col.sort);
        }
    }

}

/* ************************************** */

// Create the link to the timeseries
function create_timeseries_link(row) {
    //timeseries_groups=redis;-1;redis:hits%2Bcommand:num_get;num_calls=true:true:false:false
    return `${http_prefix}/lua/monitor/redis_monitor.lua?page=historical&ifid=-1&timeseries_groups=redis;-1;redis:hits%2Bcommand:${row.command.key};num_calls=true:true:false:false`
}

/* ************************************** */

// Handles the click on the timeseries button
function click_button_timeseries(event) {
    const row = event.row;
    window.open(create_timeseries_link(row));
}

/* ************************************** */

function on_table_custom_event(event) {
    let events_managed = {
        "click_button_timeseries": click_button_timeseries,
    };
    if (events_managed[event.event_id] == null) {
        return;
    }
    events_managed[event.event_id](event);
}

/* ************************************** */


</script>

<!-- (C) 2022 - ntop.org     -->
<template>
  <modal ref="modal_id">
    <template v-slot:title>{{ title }}</template>
    <template v-slot:body>
      <form>
        <div class="row">
          <div class="col-sm-2 pe-0 me-1">
            <SelectSearch v-model:selected_option="selected_l4_proto" :options="props.l4_proto_list">
            </SelectSearch>
          </div>
          <div ref="client_ref" class="col-sm-2 p-0 me-1">
            <input v-model="client" class="form-control" type="text" :placeholder="client_place_holder" required />
          </div>
          <template v-if="!is_arp_proto">
            <div class="col-sm-2 p-0">
              <input v-model="server" class="form-control" type="text" :placeholder="server_place_holder" required />
            </div>
            <template v-if="selected_l4_proto.id == 6 || selected_l4_proto.id == 17">
              <div v-if="rule_application_type" class="col-sm-2 p-0 ms-1">
                <SelectSearch v-model:selected_option="selected_l7_proto" :options="props.l7_proto_list">
                </SelectSearch>
              </div>
              <div v-else class="col-sm-2 p-0 ms-1">
                <input v-model="port" class="form-control" type="text" :placeholder="port_place_holder" />
              </div>
              <div class="btn-group m-auto align-items-center col-2" role="group">
                <input id="use_port" class="btn-check btn-primary" type="radio" @click="change_to_port_type" />
                <label ref="use_port_ref" class="btn btn-sm btn-primary" for="use_port">{{ _i18n('acl_page.use_port')
                  }}</label>
                <input id="use_application" class="btn-check btn-primary" type="radio" @click="change_to_app_type" />
                <label ref="use_application_ref" class="btn btn-sm btn-secondary" for="use_application">{{
                  _i18n('acl_page.use_application') }}</label>
              </div>
            </template>
          </template>
          <div class="col-sm-8 mt-2">
            <input v-model="notes" class="form-control" type="text" :placeholder="notes_placeholder" />
          </div>
        </div>
      </form>
      <div class="form-group">
        <NoteList v-if=!is_arp_proto :note_list="note_list"></NoteList>
        <NoteList v-else :note_list="note_list_arp"></NoteList>
      </div>
    </template>
    <template v-slot:footer>
      <div v-if="show_feedback" class="me-auto w-100 text-danger">{{ error }}</div>
      <div v-if="show_feedback" class="mt-1 notes bg-danger me-auto w-100 bg-opacity-25">
        {{ feedback }}
      </div>
      <div>
        <Spinner :show="activate_edit_spinner" size="1rem" class="me-2"></Spinner>
        <button type="button" @click="edit_" class="btn btn-primary" :disabled="disable_add">{{ _i18n('edit')
          }}</button>
      </div>
    </template>
  </modal>
</template>

<script setup>
import { ref, watch, onBeforeMount, onMounted } from "vue";
import { default as modal } from "./modal.vue";
import { default as SelectSearch } from "./select-search.vue";
import { default as NoteList } from "./note-list.vue";
import dataUtils from "../utilities/data-utils"
import { default as Spinner } from "./spinner.vue";

const modal_id = ref(null);
const emit = defineEmits(['edit']);
const _i18n = (t) => i18n(t);
const disable_add = ref(false)
const rules_to_add = ref('')
const client = ref(null)
const server = ref(null)
const port = ref(null)
const client_place_holder = ref(_i18n('client'))
const server_place_holder = ref(_i18n('server'))
const notes_placeholder = ref(_i18n('acl_page.notes'))
const port_place_holder = ref(_i18n('port'))
const show_feedback = ref(false);
const activate_edit_spinner = ref(false);
const feedback = ref('');
const error = ref(i18n('acl_page.error_detected'))
const title = ref(i18n('acl_page.edit_acl_rule'));
const selected_l4_proto = ref([])
const selected_l7_proto = ref([])
const row_key = ref(null)
const rule_port_type = ref(false)
const rule_application_type = ref(false)
const use_port_ref = ref(null);
const use_application_ref = ref(null);
const is_arp_proto = ref(false);
const client_ref = ref(null)
const notes = ref(null)

const note_list = [
  _i18n("acl_page.edit_acl_required"),
  _i18n("acl_page.edit_acl_empty_port_app"),
  _i18n("acl_page.edit_acl_switch_port_app"),
  _i18n("acl_page.edit_acl_notes"),
]

const note_list_arp = [
  _i18n("acl_page.edit_arp_only_client"),
  _i18n("acl_page.edit_arp_use_mac"),
  _i18n("acl_page.edit_acl_notes"),
]

const showed = () => { };

/* ************************************** */

const props = defineProps({
  context: Object,
  url_request: String,
  l4_proto_list: Array,
  l7_proto_list: Array,
});

/* ************************************** */

watch(() => selected_l4_proto.value, (cur_value) => {
  if (cur_value.id == 'arp') {
    is_arp_proto.value = true
    client_ref.value.classList.add('col-sm-4')
    client_ref.value.classList.remove('col-sm-2')
  } else {
    is_arp_proto.value = false
    rule_port_type.value = true
    client_ref.value.classList.remove('col-sm-4')
    client_ref.value.classList.add('col-sm-2')
  }
}, { flush: 'pre' });


/* ************************************** */

function change_to_port_type() {
  rule_port_type.value = true;
  rule_application_type.value = false;

  use_port_ref.value.classList.add('btn-primary')
  use_port_ref.value.classList.remove('btn-secondary')

  use_application_ref.value.classList.remove('btn-primary')
  use_application_ref.value.classList.add('btn-secondary')
}

/* ************************************** */

function change_to_app_type() {
  rule_port_type.value = false;
  rule_application_type.value = true;

  use_port_ref.value.classList.remove('btn-primary')
  use_port_ref.value.classList.add('btn-secondary')

  use_application_ref.value.classList.add('btn-primary')
  use_application_ref.value.classList.remove('btn-secondary')
  selected_l7_proto.value = props.l7_proto_list[0]
}

/* ************************************** */

function reset_modal_form(row) {
  row_key.value = row.key
  selected_l4_proto.value = props.l4_proto_list.find((t) => t.id == row.proto.id)
  if (row.l7_proto) {
    change_to_app_type()
    selected_l7_proto.value = props.l7_proto_list.find((t) => t.id == row.l7_proto.id)
    port.value = null
  } else if (row.port) {
    change_to_port_type()
    port.value = row.port
    selected_l7_proto.value = null
  }
  client.value = row.client
  server.value = row.server
  activate_edit_spinner.value = false;
  show_feedback.value = false;
  feedback.value = '';
  notes.value = row.note
}

/* ************************************** */

const show = (row) => {
  reset_modal_form(row);
  modal_id.value.show();
};

/* ************************************** */

const edit_ = async () => {
  let new_rule = ''
  if (!dataUtils.isEmptyOrNull(selected_l4_proto.value)) {
    new_rule = new_rule + '' + selected_l4_proto.value.label
  }
  if (!dataUtils.isEmptyOrNull(client.value)) {
    new_rule = new_rule + ';' + client.value
  }
  if (!dataUtils.isEmptyOrNull(server.value) && !is_arp_proto.value) {
    new_rule = new_rule + ';' + server.value
  }
  if (!dataUtils.isEmptyOrNull(port.value) && rule_port_type.value && !is_arp_proto.value) {
    new_rule = new_rule + ';' + port.value
  }
  if (!dataUtils.isEmptyArrayOrNull(selected_l7_proto.value) && rule_application_type.value && !is_arp_proto.value) {
    new_rule = new_rule + ';' + selected_l7_proto.value.label
  }
  if (!dataUtils.isEmptyOrNull(notes.value)) {
    new_rule = new_rule + '#' + notes.value
  }

  const params = {
    csrf: props.context.csrf,
    rules: new_rule,
    serial_key: row_key.value
  }

  const rsp = await ntopng_utility.http_post_request(props.url_request, params);
  activate_edit_spinner.value = false;
  if (rsp.result == 'ok') {
    show_feedback.value = false;
    emit('edit', params);
    close();
  } else {
    show_feedback.value = true;
    feedback.value = rsp.result;
  }
};

/* ************************************** */

const close = () => {
  modal_id.value.close();
};

/* ************************************** */

onBeforeMount(() => { })

defineExpose({ show, close });


</script>

<style scoped></style>

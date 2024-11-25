<!-- (C) 2022 - ntop.org     -->
<template>
  <modal ref="modal_id">
    <template v-slot:title>{{ title }}</template>
    <template v-slot:body>
      <form>
        <div class="row">
          <div class="col-sm-2 pe-0 me-2">
            <SelectSearch v-model:selected_option="selected_l4_proto" :options="props.l4_proto_list">
            </SelectSearch>
          </div>
          <div class="col-sm-2 p-0 me-2">
            <input v-model="client" class="form-control" type="text" :placeholder="client_place_holder" required />
          </div>
          <div class="col-sm-2 p-0">
            <input v-model="server" class="form-control" type="text" :placeholder="server_place_holder" required />
          </div>
          <div v-if="rule_application_type" class="col-sm-2 pe-0">
            <SelectSearch v-model:selected_option="selected_l7_proto" :options="props.l7_proto_list">
            </SelectSearch>
          </div>
          <div v-if="rule_port_type" class="col-sm-2 pe-0">
            <input v-model="port" class="form-control" type="text" :placeholder="port_place_holder" required />
          </div>
          <div class="btn-group d-flex m-auto align-items-center col-2" role="group">
            <input id="use_port" class="btn-check btn-primary" type="radio" @click="change_to_port_type"/>
            <label ref="use_port_ref" class="btn btn-sm btn-secondary" for="use_port">{{ _i18n('acl_page.use_port') }}</label>
            <input id="use_application" class="btn-check btn-primary" type="radio" @click="change_to_app_type"/>
            <label ref="use_application_ref"class="btn btn-sm btn-secondary" for="use_application">{{ _i18n('acl_page.use_application') }}</label>
          </div>
        </div>
      </form>
      <div class="form-group">
      </div>
    </template>
    <template v-slot:footer>
      <div v-if="show_feedback" class="me-auto w-100 text-danger">{{ error }}</div>
      <div v-if="show_feedback" class="mt-1 notes bg-danger me-auto w-100 bg-opacity-25">
        {{ feedback }}
      </div>
      <div>
        <Spinner :show="activate_edit_spinner" size="1rem" class="me-2"></Spinner>
        <button type="button" @click="edit_" class="btn btn-primary" :disabled="disable_add">{{ _i18n('edit') }}</button>
      </div>
    </template>
  </modal>
</template>

<script setup>
import { ref, onBeforeMount, onMounted } from "vue";
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

const note_list_advanced_settings = [
  _i18n("acl_page.each_host_separate_line"),
  _i18n("acl_page.rule_format"),
  _i18n("acl_page.non_mandatory_parameters"),
  _i18n("acl_page.select_one_parameter"),
  _i18n("acl_page.parameters_separator"),
]

const note_list_basic_settings = [
  _i18n("acl_page.each_host_separate_line"),
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
}

/* ************************************** */

function reset_modal_form(row) {
  row_key.value = row.key
  selected_l4_proto.value = props.l4_proto_list.find((t) => t.id == row.proto.id)
  if(row.l7_proto) {
    change_to_app_type()
    selected_l7_proto.value = props.l7_proto_list.find((t) => t.id == row.l7_proto.id)
    port.value = null
  } else {
    change_to_port_type()
    port.value = row.port
    selected_l7_proto.value = null
  }
  client.value = row.client
  server.value = row.server
  activate_edit_spinner.value = false;
  show_feedback.value = false;
  feedback.value = '';
}

/* ************************************** */

const show = (row) => {
  reset_modal_form(row);
  modal_id.value.show();
};

/* ************************************** */

const edit_ = async () => {
  let new_rule = ''
  if(!dataUtils.isEmptyOrNull(selected_l4_proto.value)) {
    new_rule = new_rule + '' + selected_l4_proto.value.label
  }
  if(!dataUtils.isEmptyOrNull(client.value)) {
    new_rule = new_rule + ':' + client.value
  }
  if(!dataUtils.isEmptyOrNull(server.value)) {
    new_rule = new_rule + ':' + server.value
  }
  if(!dataUtils.isEmptyOrNull(rule_port_type.value)) {
    new_rule = new_rule + ':' + rule_port_type.value
  }
  if(!dataUtils.isEmptyOrNull(rule_application_type.value)) {
    new_rule = new_rule + ':' + rule_application_type.value
  }

  debugger;
  const params = {
    csrf: props.context.csrf,
    rules: new_rule,
    key: row_key.value
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

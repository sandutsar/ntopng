<!-- (C) 2022 - ntop.org     -->
<template>
  <modal ref="modal_id">
    <template v-slot:title>{{ title }}</template>
    <template v-slot:body>
      <form>
        <div class="row">
          <label class="col-form-label col-sm-3 pe-0" id="advanced-view">
            <b>{{ advanced_settings }}</b>
          </label>
          <div class="col-sm-2 ps-0">
            <div class="form-check form-switch mt-2" id="advanced-view">
              <input v-model="advanced_settings_enabled" name="show_advanced_settings" class="form-check-input"
                type="checkbox" role="switch">
            </div>
          </div>
        </div>
        <template v-if="advanced_settings_enabled">
          <div class="form-group ms-2 me-2 mt-2 row">
            <textarea rows="10" cols="10" style="width: 100%; height: 100%;" v-model="rules_to_add"></textarea>
          </div>
        </template>
      </form>
      <div class="form-group">
        <NoteList v-if=advanced_settings_enabled :note_list="note_list_advanced_settings"></NoteList>
        <NoteList v-else :note_list="note_list_basic_settings"></NoteList>
      </div>
    </template>
    <template v-slot:footer>
      <div v-if="show_feedback" class="me-auto w-100 text-danger">{{ error }}</div>
      <div v-if="show_feedback" class="mt-1 notes bg-danger me-auto w-100 bg-opacity-25">
        {{ feedback }}
      </div>
      <div>
        <Spinner :show="activate_add_spinner" size="1rem" class="me-2"></Spinner>
        <button type="button" @click="add_" class="btn btn-primary" :disabled="disable_add">{{ _i18n('add') }}</button>
      </div>
    </template>
  </modal>
</template>

<script setup>
import { ref, onBeforeMount, onMounted } from "vue";
import { default as modal } from "./modal.vue";
import { default as SelectSearch } from "./select-search.vue";
import { default as NoteList } from "./note-list.vue";
import { default as Spinner } from "./spinner.vue";

const modal_id = ref(null);
const emit = defineEmits(['add']);
const _i18n = (t) => i18n(t);
const disable_add = ref(false)
const rules_to_add = ref('')
const advanced_settings_enabled = ref(true)
const advanced_settings = ref(i18n('acl_page.advanced_settings'))
const show_feedback = ref(false);
const activate_add_spinner = ref(false);
const feedback = ref('');
const error = ref(i18n('acl_page.error_detected'))
const title = ref(i18n('acl_page.add_acl_rule'));

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
});

/* ************************************** */

function reset_modal_form() {
  activate_add_spinner.value = false;
  show_feedback.value = false;
  rules_to_add.value = '';
  feedback.value = '';
}

/* ************************************** */

const show = (row) => {
  reset_modal_form();
  modal_id.value.show();
};

/* ************************************** */

const add_ = async () => {
  activate_add_spinner.value = true;
  const params = {
    csrf: props.context.csrf,
    rules: rules_to_add.value
  }
  const rsp = await ntopng_utility.http_post_request(props.url_request, params);
  activate_add_spinner.value = false;
  if(rsp.result == 'ok') {
    show_feedback.value = false;
    emit('add', params);
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

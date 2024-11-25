<!-- (C) 2022 - ntop.org     -->
<template>
  <modal ref="modal_id">
    <template v-slot:title>
      {{ _i18n("acl_page.delete_acl_rule") }}
    </template>
    <template v-slot:body>
      {{ message }}
    </template><!-- modal-body -->
    <template v-slot:footer>
      <button type="button" @click="delete_host" class="btn btn-danger">{{ _i18n("delete") }}</button>
    </template>
  </modal>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { default as modal } from "./modal.vue";
import { ntopng_utility } from "../services/context/ntopng_globals_services";

const _i18n = (t) => i18n(t);
const modal_id = ref(null);
const message = ref(i18n('acl_page.delete_confirmation'))
const emit = defineEmits(["delete_rule"]);
const row_key = ref({});
const props = defineProps({
  context: Object,
});

onMounted(() => { });

async function delete_host() {
  const url = `${http_prefix}/lua/pro/rest/v2/delete/system/access_control_list.lua`;
  const params = {
    csrf: props.context.csrf,
    serial_key: row_key.value,
  };

  let headers = {
    'Content-Type': 'application/json'
  };
  await ntopng_utility.http_request(url, { method: 'post', headers, body: JSON.stringify(params) });
  emit('delete_rule', params);
  close();
}

const show = (row) => {
  row_key.value = row.key
  message.value = i18n('acl_page.delete_confirmation') + ": " + (row.rule || "") + "?"
  modal_id.value.show();
};

const close = () => {
  modal_id.value.close();
};

defineExpose({ show, close });

</script>

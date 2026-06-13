<script setup>
import { onMounted } from 'vue';
import {useGroupStore} from '../stores/useGroupStore.js'
import { useAssetStore } from '../stores/useAssetStore.js';

const groupStore=useGroupStore()
const assetStore=useAssetStore()

onMounted(()=>{
    groupStore.fetchGroups()
    assetStore.fetchAssets()
})

</script>

<template>
    <RouterView />
</template>

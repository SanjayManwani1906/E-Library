<script setup>
import { RouterLink } from 'vue-router'
import { useRoute } from 'vue-router'
import { ref, watch } from 'vue'


const route = useRoute()
let section = ref({})

function addSection() {

    if (!section.value.Name) {
        return alert("Section Name cannot be empty")
    }

    var jd = {
        "sectionname": section.value.Name,
        "description": section.value.Description
    }

    fetch("http://127.0.0.1:5000/createsection?token=" + route.params.token, {
        method: "POST",
        body: JSON.stringify(jd),
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(json => {
            alert(json.Alert)
        })
}

</script>

<template>
    <main>
        <div style="display: flex; flex-direction: row;justify-content:space-between;">
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;">
            
            <h1 class="title" style="margin-top: 8px;font-size:35px">
                Add {{ section.Name }}
            </h1>
            
            <img src="/src/assets/static/BL.png" width="65" height="65" style="margin:10px; margin-bottom: 5px;opacity: 0;">
        </div>
        <div align="center">
            <div style="margin: 15px;">
                <RouterLink :to="{ name: 'adminhome', params: { token: route.params.token } }" class="new">
                    Home
                </RouterLink>
                <RouterLink :to="{ name: 'login' }" class="new">
                    Log-Out
                </RouterLink>
            </div>
        </div>

        <br>
        <div align='center'>
            <div align='center' class="post-form">
                <br>

                <label for='name'>Section Name</label>
                <br>
                <input id='name' type='text' name="name" maxlength="25" v-model="section.Name" required>

                <br>
                <br>
                <label for='description'>Section Description</label>
                <br>
                <input id='description' type='text' name="description" maxlength="100" v-model="section.Description"
                    required>
                <br>
                <br>
            </div>
            <br>
            <br>
            <button @click="addSection" class="new" style="margin-bottom:10px;margin-top:10px;font-size: 20px;">
                Save Section
            </button>

        </div>
    </main>
</template>

<style scoped>
.chapter {
    border: 1px white solid;
    border-radius: 20px;
    margin: 15px;
    margin-top: 20px;
    padding: 20px;
    display: flex-box;
    width: fit-content;
    background: rgba(0, 0, 0, 0.5);
}

.post-form {
    display: inline-table;
    padding: 10px;
    border: 0.75px solid grey;
    border-radius: 22px;
    width: 222px;
    background: rgba(0, 0, 0, 0.7);
}

input[type='file'] {
    color: rgba(0, 0, 0, 0)
}
</style>
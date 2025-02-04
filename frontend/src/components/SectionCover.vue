<script setup>
import { RouterLink } from 'vue-router';
import { defineProps } from "vue"
import { ref, onUpdated } from 'vue'


const props = defineProps(["section", "token", "authorisation"])

function deleteSection(sid) {
    console.log("Delete Clicked")
    fetch("http://127.0.0.1:5000/deletesection/" + sid + "?token=" + props.token, {
        method: "GET",
        headers: {
            "Content-type": "application/json",
        }
    })
        .then((response) => response.json())
        .then((data) => {
            console.log(data.Alert)
        })
}

</script>

<template>
    
        <div class="post">
            <table style="margin: auto;">

                <tr>
                    <td style="font-size: large;font-weight: bolder;">
                        <h2>{{ section.Name }}</h2>
                    </td>
                </tr>
                <tr>
                    <td style="color: gray;">
                        {{ section.Description }}
                    </td>
                </tr>
                <tr v-if="authorisation='admin'">
                    <td style="padding-top:0px;font-size:15px;">
                        <button @click.stop.prevent class="new">
                            Edit Section
                        </button>
                        <button  @click.stop.prevent="deleteSection(section.Id)" class="new">
                            Delete Section
                        </button>
                    </td>
                </tr>
            </table>
        </div>

    
</template>
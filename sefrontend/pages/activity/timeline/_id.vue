<template>
    <div class="container">

        <v-card>
            <v-card-title class="cyan darken-1">
                <v-spacer></v-spacer>
                <span class="headline white--text">{{ activity.title }}</span>
                <v-spacer></v-spacer>


            </v-card-title>
        </v-card>

        <v-data-table
            :headers="headers"
            :items="data"
            :items-per-page="25"
            @click:row="tableRow_Click"
            class="elevation-1 clickable"
        >
            <template v-slot:top>
                <v-toolbar
                    flat
                >
                    <v-spacer></v-spacer>
                    <v-toolbar-title>กำหนดการของกิจกรรม</v-toolbar-title>
                    <v-spacer></v-spacer>
                     <v-btn
                        v-if="edit"
                        color="info"
                        dark
                        class="mb-2"
                        @click="tableRow_new"
                        >
                        เพิ่มกำหนดการ
                    </v-btn>
                </v-toolbar>
            </template>

            <template v-slot:item.actions="{ item }">
                <v-icon
                    small
                    @click="tableRow_Remove(item)"
                >
                    mdi-delete
                </v-icon>
            </template>
        </v-data-table>


        <p class="text-center pt-2">
            <v-btn @click="goBack" color="warning"> ย้อนกลับ </v-btn>
        </p>
    </div>
</template>
<script>

const PAGE_LIST_URL = '/activity/all'

export default {
    data() {
        const headers = [
            { value: "index", text: "ลำดับที่", align: "center" },
            { value: "description", text: "รายละเอียด", align: "left" },
            { value: "lecturer_name", text: "ผู้บรรยาย", align: "center" },
            { value: "start_datetime_text", text: "เริ่มต้น", align: "center" },
            { value: "end_datetime_text", text: "สิ้นสุด", align: "center" },
            { value: 'actions', text: '', sortable: false },
        ];
        return { headers: headers, data: [ ], activity: {}, edit: false }
    },

    async asyncData({$axios, params}) {
        try {
            var user_id = parseInt(localStorage.getItem('user_id'));

            const id = params.id;
            const activity =  await $axios.$get('/api/v1/activity/' + id + '/');
            const timelines = await $axios.$get('/api/v1/timeline/?activity=' + id);

            // format data
            var index = 1;
            var rows = timelines.map( function(row) {
                row.index = index++;
                if (row.start_datetime)
                    row.start_datetime_text = formatTimeText( row.start_datetime );
                if (row.end_datetime)
                    row.end_datetime_text = formatTimeText( row.end_datetime );
                return row;
            });
            return { activity: activity, data: rows, edit: (activity.userprofile == user_id ) };
        } catch(error) {
            alert(error);
            this.$router.go(-1);
        }

    },

    methods: {

        tableRow_new() {
            this.$router.push( "/activity/timeline/edit/" + this.activity.id );
            //window.location.href = "/activity/timeline/edit/" + this.activity.id;
        },

        tableRow_Click(value) {
          //console.log(value);
          //this.$router.push( "/activity/" + value.id );
        },

        tableRow_Remove(item) {
            var context = this;

            if (confirm("ต้องการลบรายการนี้ ?")) {

                context.$axios.$delete('/api/v1/timeline/' + item.id + '/')
                    .then(function() {
                        alert('ลบข้อมูลสำเร็จ');
                        //context.$router.push('/activity/all');
                        context.$nuxt.refresh();
                    })

                    .catch(function(err) {
                        alert(err);
                    });
                //this.$router.push( "/activity/remove/" + item.id );
            }

        },

        table_Print() {
            window.print()
        },

        table_Export(data, headers) {
            var out_headers = {};
            headers.map( function(item) {
                out_headers[item.value] = item.text || item.value;
            });

            var out_rows = data;
            exportDataToCSV(out_rows, out_headers);
        },

        goBack() {
            return this.$router.go(-1);
        }
    }
};
</script>
<style scoped>
.container {
  padding: 1em;
  width: 1220px;
  margin: 0 auto;
}

.clickable table tr td:hover { cursor: pointer }
</style>

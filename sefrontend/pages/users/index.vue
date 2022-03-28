<template>
    <div class="container">
        <v-data-table
            :headers="headers"
            :items="data"
            :items-per-page="25"            
            class="elevation-1 clickable"
        >
            <template v-slot:top>
                <v-toolbar                    
                    flat
                >
                    <v-spacer></v-spacer>
                    <v-toolbar-title>สรุปกิจกรรมทั้งหมด</v-toolbar-title>
                    <v-spacer></v-spacer>

                    <v-btn
                        color="info"
                        dark
                        class="mb-2"
                        href="/users/edit/"
                        >
                        เพิ่มสมาชิก
                    </v-btn>
                </v-toolbar>
            </template>

            <template #item.title="{ item }">
                <a @click="tableRow_Click(item)">
                {{ item.title }}
                </a>
            </template>

            <template #item.is_published="{ value }">
                <v-icon
                    v-if="value"
                    small
                    class="mr-2"                    
                >   mdi-check-circle                  
                </v-icon>
            </template>

            <template v-slot:item.actions="{ item }">

                <div v-if="1">
                <v-icon
                    small
                    class="mr-2"
                    @click="tableRow_Edit(item)"
                >
                    mdi-pencil
                </v-icon>
                <v-icon
                    small
                    @click="tableRow_Remove(item)"
                >
                    mdi-delete
                </v-icon>
                </div>
            </template>
            <template v-slot:no-data>
                <div class="text-center">
                    ไม่มีข้อมูลแสดง
                </div>
            </template>
        </v-data-table>
        <div class="text-center pt-2">
            <v-btn
                color="success"
                class="mr-2"
                @click="table_Print"
            >
                Print
            </v-btn>
            <v-btn
                color="info"
                @click="table_Export(data, headers)"
            >
                Export
            </v-btn>
        </div>        

    </div>
</template>
<script>
export default {
    data() {
        const headers = [     
            { value: "index", text: "ลำดับที่", align: "center" },
            { value: "profile_type", text: "ประเภท", align: "left" },
            { value: "member_id", text: "รหัสนักศึกษา/อาจารย์", align: "left" },
            { value: "fullname", text: "ชื่อ-สกุล", align: "center" },
            { value: "faculty", text: "สาข่า", align: "center" },
            { value: "contract", text: "ติดต่อ", align: "center" },
            { value: "facebook", text: "เฟสบุ๊ค", align: "center" },
            { value: "picture", text: "รูป", align: "center" },
            { value: "created_at", text: "วันที่ประกาศ", align: "center" },
            { value: 'actions', text: '', sortable: false },
        ];
        return { headers: headers, data: [ ] }
    },

    async asyncData({$axios, redirect}) {
        var user_id = parseInt(localStorage.getItem('user_id'));
        if (!user_id || user_id <= 0) {
            alert('โปรดเข้าสู่ระบบก่อน');
            redirect('/login');
            return;
        }

        const results = await $axios.$get('/api/v1/userprofile/');

        // format data
        var index = 1;
        var rows = results.map( function(row) {
            row.index = index++;
            if (row.created_at) 
                row.created_at = formatDateTimeText( row.created_at );
            row.profile_type = (row.profile_type == 'teacher') ? "อาจารย์" : "สมาชิก";
            //console.log('row', row);
            return row;
        });
        return { data: rows };
    },

    methods: {

        tableRow_Click(item) {
            //console.log(value);
            this.$router.push( "/users/edit/" + item.id );
        },

        tableRow_QRCode(item) {
            window.open( item.qrcode_url, '_blank' );
        },

        tableRow_Edit(item) {
            this.$router.push( "/users/edit/" + item.id );
        },

        tableRow_Remove(item) {
            var context = this;

            if (confirm("ต้องการลบรายการนี้ ?")) {

                context.$axios.$delete('/api/v1/userprofile/' + item.id + '/')
                    .then(function() {
                        alert('บันทึกข้อมูลสำเร็จ');
                        //context.$router.push('/activity/all');                    
                        context.$nuxt.refresh();
                    })

                    .catch(function(err) {
                        alert(err);
                    });
                //this.$router.push( "/activity/remove/" + item.id );
            }
            
        },

        table_Export(data, headers) {
            var out_headers = {};
            headers.map( function(item) {
                out_headers[item.value] = item.text || item.value;
            });

            var out_rows = data;
            exportDataToCSV(out_rows, out_headers);
        },

        table_Print() {
            window.print()
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

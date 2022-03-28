<template>
    <div class="container">
        <v-toolbar                    
            flat
        >
            <v-spacer></v-spacer>
            <v-toolbar-title>กำหนดสมาชิก</v-toolbar-title>
            <v-spacer></v-spacer>
                <v-btn
                v-if="edit"
                color="info"
                dark
                class="mb-2"
                @click="tableRow_new"
                >
                เพิ่มสมาชิก
            </v-btn>
        </v-toolbar>
        
        <form @submit.prevent="submitData">
            <v-select
                v-model="profile_type"
                :items="profile_types"
                item-value="value"
                item-text="text"
                label="ประเภท"
                required
            ></v-select>
            <v-text-field
                v-model="member_id"
                label="รหัสประจำตัว"
                required
            ></v-text-field>
            <v-text-field
                v-model="fullname"
                label="ชื่อ-สกุล"
                required
            ></v-text-field>
            <v-text-field
                v-model="faculty"
                label="สาขา"
                required
            ></v-text-field>
            <v-text-field
                v-model="contract"
                label="ติดต่อ"
                required
            ></v-text-field>  
             <v-text-field
                v-model="facebook"
                label="เฟสบุ๊ค"
            ></v-text-field>
            <v-divider />
            <v-text-field
                v-model="password"
                type="password"
                label="รหัสผ่าน"
            ></v-text-field>            

            <div class="text-center">
                <v-btn class="text-center" type="submit" color="primary" :disabled="loading"> 
                    บันทึก 
                    <template v-slot:loader>
                      <span>กำลังบันทึก...</span>
                    </template>
                </v-btn>

                <v-btn @click="goBack" color="warning"> ย้อนกลับ </v-btn>
            </div>
        </form>
    </div>
</template>
<script>

const PAGE_LIST_URL = "/users/";

const WEBAPI_GET_URL = "/api/v1/userprofile/";
const WEBAPI_CREATE_URL = "/api/v1/userprofile/";
const WEBAPI_UPDATE_URL = "/api/v1/userprofile/";
const WEBAPI_DELETE_URL = "/api/v1/userprofile/";

export default {
    data() {
        var user_id = parseInt(localStorage.getItem('user_id'));
        if (!user_id || user_id <= 0) {
            alert('โปรดเข้าสู่ระบบก่อน');
            this.$router.push('/login');
            return;
        }

        return {  
            loading: false, 
            user_id: user_id,                       
            id: 0,
            profile_type: 'member',
            member_id: '',
            fullname: '',
            contract: '',
            facebook: '',
            picture: '',
            password: '',
            profile_types: [
                { "value": "member", "text": "สมาชิก" }, 
                { "value": "teacher", "text": "อาจารย์" } 
            ]
        }
    },

    async asyncData({ $axios, params }) {
        var id = params.id || 0; 
        var results = {};

        var data = {};
        if (id > 0) {
            data = await $axios.$get(WEBAPI_GET_URL + id + '/')
            //console.log('edit', results);
            results.id = id;
        }

        return  Object.assign(results, data);
    },

    methods: {
        submitData() {
            var context = this;
            var params = context.params;
            var data = {
                profile_type: this.profile_type,
                member_id: this.member_id,
                fullname: this.fullname,
                contract: this.contract,
                facebook: this.facebook,
                picture: this.picture,
                password: this.password
            };
            //console.log(data);

            var id = this.id;
            if (id > 0) {

                context.$axios.$put(WEBAPI_UPDATE_URL + id + '/', data)
                    .then(function() {
                        alert('บันทึกข้อมูลสำเร็จ');
                        context.$router.push(PAGE_LIST_URL);                    
                    })

                    .catch(function(err) {
                        alert(err);
                    });

            } else {

                context.$axios.$post(WEBAPI_CREATE_URL + '/', data)
                    .then(function() {
                        alert('บันทึกข้อมูลสำเร็จ');
                        context.$router.push(PAGE_LIST_URL);                    
                    })

                    .catch(function(err) {
                        alert(err);
                    });
            }
        },

        goBack() {
            return this.$router.go(-1);
        }
    },
}
</script>
<style scoped>
.container {
  padding: 1em;
  width: 1220px;
  margin: 0 auto;
}

.clickable table tr td:hover {
  cursor: pointer;
}
</style>

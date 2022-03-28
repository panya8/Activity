<template>
  <div class='container justify-center'>


    <v-toolbar
      flat
    >
      <v-spacer></v-spacer>

      <v-tooltip bottom>
        <template v-slot:activator='{ on, attrs }'>
          <v-btn
            color='primary'
            dark
            v-bind='attrs'
            v-on='on'
          >
            นิสิต
          </v-btn>
        </template>
        <span>สำหรับนิสิต</span>
      </v-tooltip>

      <v-divider class='ml-5 mr-5'
                 vertical
      ></v-divider>

      <v-tooltip bottom>
        <template v-slot:activator='{ on, attrs }'>
          <v-btn
            color='blue-grey lighten-3'
            dark
            v-bind='attrs'
            v-on='on'
          >
            อาจารย์
          </v-btn>
        </template>
        <span>สำหรับอาจารย์</span>
      </v-tooltip>

      <v-spacer></v-spacer>
    </v-toolbar>


    <v-row justify='center'>
      <v-col cols='12'
             sm='4'
             md='6'
             lg='8'>

        <v-card>
          <v-card-text>

            <v-toolbar
              flat
            >
              <v-spacer></v-spacer>
              <v-toolbar-title>สมัครสมาชิกใหม่สำหรับ "นิสิต"</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>


            <form @submit.prevent='submitData'>

              <!--              <v-text-field-->
              <!--                v-model='member_id'-->
              <!--                label="กรอก 'รหัสนิสิต' สำหรับนิสิต / 'ชื่อผู้ใช้' สำหรับอาจารย์"-->
              <!--                required-->
              <!--              ></v-text-field>-->

              <v-text-field
                v-model='member_id'
                label='รหัสนิสิต'
                required
              ></v-text-field>

              <v-text-field
                v-model='fullname'
                label='ชื่อ-สกุล'
                required
              ></v-text-field>

              <v-text-field
                v-model='faculty'
                label='สาขา'
                required
              ></v-text-field>

              <v-text-field
                v-model='contract'
                label='เบอร์ติดต่อ'
                required
              ></v-text-field>
              <v-text-field
                v-model='facebook'
                label='เฟสบุ๊ค'
              ></v-text-field>
              <v-text-field
                v-model='password'
                type='password'
                label='รหัสผ่าน'
              ></v-text-field>

              <div class='text-center'>
                <v-btn class='text-center' type='submit' color='primary' :disabled='loading'>
                  บันทึก
                  <template v-slot:loader>
                    <span>กำลังบันทึก...</span>
                  </template>
                </v-btn>

                <v-btn @click='goBack' color='warning'> ย้อนกลับ</v-btn>
              </div>
            </form>

          </v-card-text>
        </v-card>
      </v-col>

    </v-row>
  </div>
</template>
<script>

const PAGE_LIST_URL = '/users/'

const WEBAPI_GET_URL = '/api/v1/userprofile/'
const WEBAPI_CREATE_URL = '/api/v1/userprofile/'
const WEBAPI_UPDATE_URL = '/api/v1/userprofile/'
const WEBAPI_DELETE_URL = '/api/v1/userprofile/'

export default {
  data() {
    var user_id = parseInt(localStorage.getItem('user_id'))
    if (user_id && user_id > 0) {
      window.location.href = '/activity'
      return
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
      password: ''
    }
  },

  async asyncData({ $axios, params }) {
    var id = params.id || 0
    var results = {}

    var data = {}
    if (id > 0) {
      data = await $axios.$get(WEBAPI_GET_URL + id + '/')
      //console.log('edit', results);
      results.id = id
    }

    return Object.assign(results, data)
  },

  methods: {
    submitData() {
      var context = this
      var params = context.params
      var data = {
        profile_type: 'member',
        member_id: this.member_id,
        fullname: this.fullname,
        contract: this.contract,
        facebook: this.facebook,
        picture: this.picture,
        password: this.password
      }
      //console.log(data);

      context.$axios.$post(WEBAPI_CREATE_URL + '/', data)
        .then(function() {
          alert('บันทึกข้อมูลสำเร็จ')
          context.$router.push(PAGE_LIST_URL)
        })

        .catch(function(err) {
          alert(err)
        })
    },

    goBack() {
      return this.$router.go(-1)
    }
  }
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

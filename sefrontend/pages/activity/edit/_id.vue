<template>
  <div class='container'>

    <v-toolbar
      flat
    >
      <v-spacer></v-spacer>
      <v-toolbar-title>สร้างกิจกรรม</v-toolbar-title>
      <v-spacer></v-spacer>

    </v-toolbar>
    <v-card class='mt-5'>

      <v-stepper v-model='e1'>
        <v-stepper-header>
          <v-stepper-step
            :complete='e1 > 1'
            step='1'
          >
            กรอกข้อมูลกิจกรรม
          </v-stepper-step>

          <v-divider></v-divider>

          <v-stepper-step
            :complete='e1 > 2'
            step='2'
          >
            กรอกกำหนดการ
          </v-stepper-step>

        </v-stepper-header>

        <v-stepper-items>
          <v-stepper-content step='1'>


            <div class='mb-10 ml-10 mr-10 mt-4'>
              <form @submit.prevent='submitData'>
                <v-text-field
                  v-model='title'
                  label='หัวข้อกิจกรรม'
                  required
                ></v-text-field>
                <v-select
                  v-model='activity_type'
                  :items='activity_types'
                  label='ประเภท'
                  required
                ></v-select>
                <v-textarea
                  v-model='description'
                  label='รายละเอียดกิจกรรม'
                  required
                ></v-textarea>
                <v-text-field
                  v-model='lecturer_name'
                  label='วิทยากร'
                  required
                ></v-text-field>
                <v-text-field
                  v-model='day_start'
                  label='วันที่จัดกิจกรรม เช่น "31-12-2565"'
                  required
                ></v-text-field>
                <v-checkbox
                  v-model='is_published'
                  label='เผยแพร่กิจกรรม'
                ></v-checkbox>

                <div class='text-center'>
                  <v-btn
                    class='text-center' type='submit' color='primary' :disabled='loading'>
                    บันทึก
                    <template v-slot:loader>
                      <span>กำลังบันทึก...</span>
                    </template>
                  </v-btn>

                  <v-btn @click='goBack' color='warning'> ย้อนกลับ</v-btn>
                </div>
              </form>
            </div>

          </v-stepper-content>

          <v-stepper-content step='2'>
            <v-card
              class='mb-12'
              color='grey lighten-1'
              height='200px'
            ></v-card>

            <v-btn
              color='primary'
              @click='e1 = 3'
            >
              Continue
            </v-btn>

            <v-btn text>
              Cancel
            </v-btn>
          </v-stepper-content>

        </v-stepper-items>
      </v-stepper>


    </v-card>
  </div>
</template>
<script>
const PAGE_ADD_TIMELINE = '/activity/timeline/edit/'
const PAGE_LIST_ALL = '/activity/all'
const PAGE_LIST_URL = '/activity/timeline/'


const WEBAPI_GET_URL = '/api/v1/activity/'
const WEBAPI_CREATE_URL = '/api/v1/activity/'
const WEBAPI_UPDATE_URL = '/api/v1/activity/'
const WEBAPI_DELETE_URL = '/api/v1/activity/'

export default {
  data() {
    var user_id = parseInt(localStorage.getItem('user_id'))
    if (!user_id || user_id <= 0) {
      alert('โปรดเข้าสู่ระบบก่อน')
      this.$router.push('/login')
      return
    }

    return {
      loading: false,
      user_id: user_id,
      id: 0,
      title: '',
      description: '',
      lecturer_name: '',
      day_start:'',
      is_published: false,
      activity_type: '',
      activity_types: [],
      e1: 1
    }
  },

  async asyncData({ $axios, params }) {
    var id = params.id || 0
    var results = {}

    console.log('params', params)

    var activity_types = await $axios.$get(`/api/v1/activity_type/`)
    results.activity_types = activity_types.map(function(row) {
      return { value: row.id, text: row.activity_type_name }
    })

    var data = {}
    if (id > 0) {
      data = await $axios.$get(WEBAPI_GET_URL + id + '/')
      console.log('edit', results)
      results.id = id
    }

    return Object.assign(results, data)
  },

  methods: {
    submitData() {
      var context = this
      var params = context.params
      var data = {
        title: this.title,
        description: this.description,
        activity_type: this.activity_type,
        lecturer_name: this.lecturer_name,
        is_published: this.is_published,
        day_start: this.day_start,
        userprofile: this.user_id
      }
      console.log(data)

      var id = this.id
      if (id > 0) {

        context.$axios.$put(WEBAPI_UPDATE_URL + id + '/', data)
          .then(function() {
            alert('บันทึกข้อมูลสำเร็จ')
            context.$router.push('/activity/' + id)
          })

          .catch(function(err) {
            alert(err)
          })

      } else {

        context.$axios.$post(WEBAPI_CREATE_URL + '/', data)
          .then(function(event) {
            alert('บันทึกข้อมูลสำเร็จ')
            context.$router.push('/activity/my')

          })

          .catch(function(err) {
            alert(err)
          })
      }
    },
    tableRow_new() {
      this.$router.push('/activity/timeline/edit/my')
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

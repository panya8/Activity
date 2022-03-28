<template>
  <div class='container'>

    <div class='container'>

      <v-toolbar
        flat
      >
        <v-spacer></v-spacer>
        <v-toolbar-title>เพิ่มกำหนดการ กิจกรรม: {{ activity.title }}</v-toolbar-title>
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


            </v-stepper-content>

            <v-stepper-content step='2'>

              <div class='mb-10 ml-10 mr-10 mt-4'>
                <form @submit.prevent='submitData'>
                  <v-textarea
                    v-model='description'
                    label='กิจกรรม'
                    required
                  ></v-textarea>
                  <v-text-field
                    v-model='lecturer_name'
                    label='วิยากร'
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model='start_datetime_text'
                    label='เวลาเริ่มต้น'
                    required
                  ></v-text-field>
                  <v-text-field
                    v-model='end_datetime_text'
                    label='เวลาสิ้นสุด'
                    required
                  ></v-text-field>

                  <div class='text-center'>
                    <v-btn class='text-center' type='submit' color='primary' :disabled='loading'>
                      บันทึก
                      <template v-slot:loader>
                        <span>กำลังบันทึก...</span>
                      </template>
                    </v-btn>

                    <v-btn onclick="history.back()" color='warning'> ย้อนกลับ</v-btn>
                  </div>
                </form>
              </div>
            </v-stepper-content>

          </v-stepper-items>
        </v-stepper>


      </v-card>
    </div>


  </div>
</template>
<script>

const PAGE_LIST_URL = '/activity/'

const WEBAPI_GET_URL = '/api/v1/timeline/?activity='
const WEBAPI_CREATE_URL = '/api/v1/timeline/'
const WEBAPI_UPDATE_URL = '/api/v1/timeline/'
const WEBAPI_DELETE_URL = '/api/v1/timeline/'

export default {
  data() {
    var user_id = parseInt(localStorage.getItem('user_id'))
    if (user_id <= 0) {
      return this.$router.push('/login')
    }

    return {
      loading: false,
      user_id: user_id,
      id: 0,
      activity_id: 0,
      activity: {},
      description: '',
      lecturer_name: '',
      start_datetime: '',
      end_datetime: '',
      start_datetime_text: '',
      end_datetime_text: '',
      e1: 2

    }
  },

  async asyncData({ $axios, params }) {
    try {
      var user_id = parseInt(localStorage.getItem('user_id'))
      var activity_id = params.id || 0
      var results = {}

      console.log('params', params)

      var activity = await $axios.$get(`/api/v1/activity/` + activity_id + '/')

      if (activity.userprofile != user_id)
        throw new Error('ไม่สามารถแก้ไขรายการนี้ได้')

      console.log('activity', activity)
      results.activity = activity

      var data = {}
      if (activity_id > 0) {
        data = await $axios.$get(WEBAPI_GET_URL + activity_id + '')
        console.log('edit', results)
        results.activity_id = activity_id
      }

    } catch (error) {
      alert(error)
      this.$router.go(-1)
    }

    return Object.assign(results, data)
  },

  methods: {
    submitData() {
      var context = this
      var activity_id = parseInt(this.activity_id)
      var data = {
        activity: activity_id,
        description: this.description,
        lecturer_name: this.lecturer_name,
        start_datetime_text: this.start_datetime_text,
        end_datetime_text: this.end_datetime_text,
        start_datetime: null,
        end_datetime: null
      }
      console.log(data)
      context.$axios.$post(WEBAPI_CREATE_URL + '', data)
        .then(function() {
          alert('บันทึกข้อมูลสำเร็จ')
          context.$router.push(PAGE_LIST_URL + activity_id)
          // context.$router.push('/activity/' +id)

        })

        .catch(function(err) {
          alert(err)
        })
    }
  },

  goBack() {
     history.back()
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

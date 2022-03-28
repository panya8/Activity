<template>
  <div class='photo-info'>

    <h3>คุณต้องการบันทึกการเข้าร่วมกิจกรรม {{ title }} ?</h3>
    <v-card class='mt-5 elevation-3 pr-5'>

      <v-container>
        <v-row no-gutters class='mt-10'>
          <v-col
            cols='4'
          >
            <div
              class='pa-2'
              outlined
              tile
            >
              ชื่อกิจกรรม :
            </div>
          </v-col>
          <v-col
            cols='8'
          >
            <v-card
              class='pa-2 rounded-lg'
              outlined
              tile
            >
              {{ title }}
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <v-container class='lighten-5'>
        <v-row no-gutters class='mt-5'>
          <v-col
            cols='4'
          >
            <div
              class='pl-2 pr-2 pt-10 pb-10'
              outlined
              tile
            >
              รายละเอียดกิจกรรม :
            </div>
          </v-col>
          <v-col
            cols='8'
          >
            <v-card
              class='pl-2 pr-2 pt-10 pb-10 rounded-lg'
              outlined
              tile
            >
              {{ description }}
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <v-container class='lighten-5'>
        <v-row no-gutters class='mt-5'>
          <v-col
            cols='4'
          >
            <div
              class='pa-2'
              outlined
              tile
            >
              วิทยากร :
            </div>
          </v-col>
          <v-col
            cols='8'
          >
            <v-card
              class='pa-2 rounded-lg'
              outlined
              tile
            >
              {{ lecturer_name }}
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <v-container class='lighten-5'>
        <v-row no-gutters class='mt-5 mb-10'>
          <v-col
            cols='4'
          >
            <div
              class='pa-2'
              outlined
              tile
            >
              วันที่จัดกิจกรรม :
            </div>
          </v-col>
          <v-col
            cols='8'
          >
            <v-card
              class='pa-2 rounded-lg'
              outlined
              tile
            >
              {{ day_start }}
            </v-card>

          </v-col>
        </v-row>
      </v-container>



    </v-card>


    <p class='text-center pt-2 mt-5'>
      <v-btn @click='participant_checkin' color='success'>บันทึกการเข้าร่วมกิจกรรมนี้</v-btn>
    </p>
    <p class='text-center pt-2'>

      <v-btn @click='goBack' class='red mb-5'>ยกเลิก</v-btn>
    </p>
  </div>
</template>
<script>

const CANCEL_URL = 'www.google.com'

export default {
  data() {
    return {}
  },

  async asyncData({ $axios, params, redirect }) {
    const row = await $axios.$get(`/api/v1/activity/${params.id}/`)
    if (!row.is_published) {
      alert('กิจกรรมนี้ไม่ได้ถูกเผยแพร่')
      redirect('/activity')
      return
    }

    if (row.created_at)
      row.created_at = formatDateTimeText(row.created_at)
    if (row.userprofile_data && row.userprofile_data.fullname)
      row.fullname = row.userprofile_data.fullname
    return row
  },

  methods: {

    timeline() {

      this.$router.push('/activity/timeline/' + this.id)
    },

    participant_checkin() {
      var user_id = parseInt(localStorage.getItem('user_id'))
      if (user_id <= 0) {
        alert('โปรดเข้าสู่ระบบก่อน')
        this.$router.push('/login')
        return
      }

      var activity = this.id
      if (activity <= 0) {
        alert('id ผิดพลาด')
        return
      }

      var data = {
        activity: activity,
        userprofile: user_id
      }
      this.$axios.post('/api/v1/participantcheckin/', data)
        .then(function() {
          alert('บันทึกข้อมูลแล้ว')
          window.close()
        })
        .catch(function(err) {
          alert('ไม่สามารถลงทะเบียนซ้ำได้')
          window.close()

        })
    },

    goBack() {
      window.close()
      alert('ยกเลิกการเข้าร่วม')
    }
  }
}
</script>
<style scoped>
.description {
  min-height: 380px;
  padding: 15px;
}

.photo-info {
  width: 860px;
  margin: 0 auto;
  text-align: center;
}

.img {
  width: 100%;
}

.link {
  display: inline-block;
  margin-top: 2em;
}
</style>

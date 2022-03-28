<template>
  <div class='photo-info'>

    <h3>รายละเอียดกิจกรรม</h3>
    <v-card class='mt-5 elevation-2 pr-5'>

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
              {{ activity.title }}
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
              {{ activity.description }}
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
              {{ activity.lecturer_name }}
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
              {{ activity.day_start }}
            </v-card>
          </v-col>
        </v-row>
      </v-container>

    </v-card>

    <v-data-table
      :headers='timeline_headers'
      :items='timelines'
      :items-per-page='25'
      @click:row='tableRow_Click'
      class='elevation-2 clickable mt-10'
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-spacer></v-spacer>
          <v-toolbar-title>กำหนดการของกิจกรรม</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn
            v-if='edit'
            color='info'
            dark
            class='mb-2'
            @click='timeline_new'
          >
            เพิ่มกำหนดการ
          </v-btn>
        </v-toolbar>
      </template>

      <template v-if='edit' v-slot:item.actions='{ item }'>
        <v-icon
          small
          @click='tableRow_Remove(item)'
        >
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>


    <p class='text-center pt-2 mt-5'>
      <v-btn @click='participant' color='success'>สนใจกิจกรรมนี้</v-btn>
    </p>
    <v-divider class='mt-5 mb-5'></v-divider>

    <p class='text-center pt-2'>
      <v-btn v-if='edit' @click='stats' color='primary'>ข้อมูลผู้เข้าร่วม</v-btn>

      <v-btn v-if='edit' @click='partiprint' color='info'>ใบเช็นชื่อ</v-btn>
    </p>

    <p class='text-center pt-2 mb-5'>

      <v-btn @click='goBack' class='warning'>ย้อนกลับ</v-btn>
    </p>
  </div>
</template>
<script>
export default {
  data() {
    const timeline_headers = [
      { value: 'index', text: 'ลำดับที่', align: 'center' },
      { value: 'description', text: 'กิจกรรม', align: 'left' },
      { value: 'lecturer_name', text: 'วิทยากร', align: 'center' },
      { value: 'start_datetime_text', text: 'เวลาเริ่มต้น', align: 'center' },
      { value: 'end_datetime_text', text: 'เวลาสิ้นสุด', align: 'center' },
      { value: 'actions', text: '', sortable: false }
    ]
    return { timeline_headers: timeline_headers, timelines: [], activity: {}, edit: false }
  },

  async asyncData({ $axios, params }) {

    try {
      var user_id = parseInt(localStorage.getItem('user_id'))

      const id = params.id
      const activity = await $axios.$get('/api/v1/activity/' + id + '/')
      const timelines = await $axios.$get('/api/v1/timeline/?activity=' + id)

      // format data
      var index = 1
      var rows = timelines.map(function(row) {
        row.index = index++
        if (row.start_datetime)
          row.start_datetime_text = formatTimeText(row.start_datetime)
        if (row.end_datetime)
          row.end_datetime_text = formatTimeText(row.end_datetime)
        return row
      })

      if (activity.created_at)
        activity.created_at = formatDateTimeText(activity.created_at)
      if (activity.userprofile_data && activity.userprofile_data.fullname)
        activity.fullname = activity.userprofile_data.fullname

      return { id: id, activity: activity, timelines: rows, edit: (activity.userprofile == user_id) }

    } catch (error) {
      alert(error)
      this.$router.go(-1)
    }
  },

  methods: {

    timeline() {

      this.$router.push('/activity/timeline/' + this.id)
    },

    timeline_new() {
      this.$router.push('/activity/timeline/edit/' + this.id)
    },

    stats() {

      this.$router.push('/activity/stats/' + this.id)
    },

    participant() {
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
      this.$axios.post('/api/v1/participant/', data)
        .then(function() {
          alert('บันทึกข้อมูลแล้ว')
        })
        .catch(function(err) {
          alert('ไม่สามารถลงทะเบียนซ้ำได้')
        })
    },

    partiprint() {

      this.$router.push('/activity/partiprint/' + this.id)
    },


    table_Print() {
      window.print()
    },

    tableRow_Remove(item) {
      var context = this

      if (confirm('ต้องการลบรายการนี้ ?')) {

        context.$axios.$delete('/api/v1/timeline/' + item.id + '/')
          .then(function() {
            alert('ลบข้อมูลสำเร็จ')
            context.$nuxt.refresh()
          })

          .catch(function(err) {
            alert(err)
          })
      }

    },


    goBack() {
      return this.$router.go(-1)
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

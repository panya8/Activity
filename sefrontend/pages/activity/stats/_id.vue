<template>
  <div class='container'>

    <v-card>
      <v-card-title class='cyan darken-1'>
        <v-spacer></v-spacer>
        <span class='headline white--text'>{{ activity.title }}</span>
        <v-spacer></v-spacer>


      </v-card-title>
    </v-card>

    <v-row>
      <v-col>
        <v-data-table
          :headers='participant_headers'
          :items='participants'
          :items-per-page='25'
          class='elevation-1 clickable'
        >
          <template v-slot:top>
            <v-toolbar
              flat
            >
              <v-spacer></v-spacer>
              <v-toolbar-title>ผู้สนใจกิจกรรมนี้</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
          </template>
        </v-data-table>

        <div class='text-center pt-2'>
          <v-btn
            color='info'
            @click='table_Export(participants, participant_headers)'
          >
            Export
          </v-btn>
        </div>
      </v-col>

      <v-col>
        <v-data-table
          :headers='checkin_headers'
          :items='checkins'
          :items-per-page='25'
          class='elevation-1 clickable'
        >
          <template v-slot:top>
            <v-toolbar
              flat
            >
              <v-spacer></v-spacer>
              <v-toolbar-title>ผู้ที่ได้เข้าร่วมกิจกรรมนี้</v-toolbar-title>
              <v-spacer></v-spacer>
            </v-toolbar>
          </template>
        </v-data-table>

        <div class='text-center pt-2'>
          <v-btn
            color='info'
            @click='table_Export(checkins, checkin_headers)'
          >
            Export
          </v-btn>
        </div>
      </v-col>
    </v-row>

    <div class='pt-2'>
      <pie-chart :data='chart_data' :options='chart_options'
                 :styles="{height: '480px', position: 'relative'}"></pie-chart>
    </div>

    <div class='text-center pt-2'>
      <v-btn
        color='success'
        class='mr-2'
        @click='table_Print'
      >
        Print
      </v-btn>
    </div>

    <p class='text-center pt-2'>
      <v-btn @click='goBack' color='warning'> ย้อนกลับ</v-btn>
    </p>
  </div>
</template>
<script>
export default {
  data() {
    const participant_headers = [
      { value: 'index', text: 'ลำดับที่', align: 'center' },
      { value: 'member_id', text: 'รหัสนักศึกษา', align: 'center' },
      { value: 'fullname', text: 'ชื่อ-สกุล', align: 'center' },
      { value: 'created_at', text: 'เวลา', align: 'center' }
    ]
    const checkin_headers = [
      { value: 'index', text: 'ลำดับที่', align: 'center' },
      { value: 'member_id', text: 'รหัสนักศึกษา', align: 'center' },
      { value: 'fullname', text: 'ชื่อ-สกุล', align: 'center' },
      { value: 'created_at', text: 'เวลา', align: 'center' }
    ]
    return {
      participant_headers: participant_headers,
      checkin_headers: checkin_headers,
      participants: [],
      checkins: [],
      activity: {},
      chart_data: {},
      chart_options: {},
      edit: false

    }
  },

  async asyncData({ $axios, params }) {
    try {
      var user_id = parseInt(localStorage.getItem('user_id'))
      if (!user_id || user_id <= 0) {
        alert('โปรดเข้าสู่ระบบก่อน')
        this.$router.push('/login')
        return
      }

      const activity_id = params.id
      const activity = await $axios.$get('/api/v1/activity/' + activity_id + '/')
      const participants = await $axios.$get('/api/v1/participant/?activity=' + activity.id)
      const checkins = await $axios.$get('/api/v1/participantcheckin/?activity=' + activity.id)

      // format data
      var index = 1
      var result_participants = participants.map(function(row) {
        console.log('row', row)
        row.index = index++
        row.member_id = row.userprofile_data.member_id
        row.fullname = row.userprofile_data.fullname
        if (row.created_at)
          row.created_at = formatTimeText(row.created_at)
        return row
      })

      var index = 1
      var result_checkins = checkins.map(function(row) {
        console.log('row', row)
        row.index = index++
        row.member_id = row.userprofile_data.member_id
        row.fullname = row.userprofile_data.fullname
        if (row.created_at)
          row.created_at = formatTimeText(row.created_at)
        return row
      })

      return {
        activity: activity,
        participants: result_participants,
        checkins: result_checkins,
        chart_data: {
          labels: ['ผู้สนใจ', 'ผุ้เข้าร่วม'],
          datasets: [{
            labels: ['ผู้สนใจ', 'ผุ้เข้าร่วม'],
            backgroundColor: [
              'rgb(255, 99, 132)',
              'rgb(54, 162, 235)',
              'rgb(255, 205, 86)'
            ],
            data: [result_participants.length, result_checkins.length]
          }],
          responsive: false,
          maintainAspectRatio: false,
          height: 480

        },
        chart_options: {
          responsive: true, // my new default options
          maintainAspectRatio: false, // my new default options
          scales: {
            yAxes: [{
              display: false
            }],
            xAxes: [{
              display: false
            }]
          }
        }

      }

    } catch (error) {
      alert(error)
      this.$router.go(-1)
    }

  },

  methods: {

    tableRow_Click(value) {
      //console.log(value);
      //this.$router.push( "/activity/" + value.id );
    },

    table_Export(data, headers) {
      var out_headers = {}
      headers.map(function(item) {
        out_headers[item.value] = item.text || item.value
      })

      var out_rows = data
      exportDataToCSV(out_rows, out_headers)
    },

    table_Print() {
      window.print()
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
  cursor: pointer
}
</style>

<template>
  <div class='container'>
    <v-card-title class='align-center justify-center'>
      <v-toolbar-title >รายชื่อผู้เข้าร่วม {{ activity.title }}</v-toolbar-title>
    </v-card-title>
    <v-card-title class='align-center justify-center'>
      <v-toolbar-subtitle >วันที่ {{ activity.day_start }}</v-toolbar-subtitle>
    </v-card-title>

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
              color='no-print'
              flat
            >
            </v-toolbar>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <div class='text-center pt-5'>
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
      { value: 'member_id', text: 'รหัสนิสิต', align: 'left' },
      { value: 'fullname', text: 'ชื่อ-สกุล', align: 'left' },
      { value: 'signature', text: 'เซ็นชื่อ', align: 'left' }
    ]
    return {
      participant_headers: participant_headers,
      participants: [],
      activity: {},
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
      const participants = await $axios.$get('/api/v1/participant/?activity=' + activity_id)

      // format data
      var index = 1
      var result_participants = participants.map(function(row) {
        console.log('row', row)
        row.index = index++
        row.member_id = row.userprofile_data.member_id
        row.fullname = row.userprofile_data.fullname
        row.created_at = ''
        return row
      })

      for (var line = index; index < 22 - result_participants.length; line++) {
        result_participants.push({ index: line })
      }

      return {
        activity: activity,
        participants: result_participants

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
@media print {
  .no-print {
    display: none !important;
  }

  button, .btn, .v-btn,
  .v-data-footer__select {
    display: none !important;
  }
}
</style>

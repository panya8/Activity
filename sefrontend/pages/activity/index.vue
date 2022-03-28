<template>
  <div class='container'>
    <v-data-table
      :headers='headers'
      :items='data'
      :items-per-page='25'
      @click:row='tableRow_Click'
      class='elevation-1 clickable'
    >
      <template v-slot:top>
        <v-toolbar
          flat
        >
          <v-spacer></v-spacer>
          <v-toolbar-title>กิจกรรมล่าสุด</v-toolbar-title>
          <v-spacer></v-spacer>

          <v-btn
            color='info'
            dark
            class='mb-2'
            href='/activity/edit/'
          >
            สร้างกิจกรรม
          </v-btn>
        </v-toolbar>
      </template>

      <template #item.title='{ item }'>
        <a @click='tableRow_Click(item)'>
          {{ item.title }}
        </a>
      </template>
    </v-data-table>

  </div>
</template>
<script>
export default {
  data() {
    const headers = [
      { value: 'index', text: 'ลำดับที่', align: 'center' },
      { value: 'day_start', text: 'วันที่จัดกิจกรรม', align: 'center' },
      { value: 'title', text: 'ชื่อกิจกรรม', align: 'left' },
      { value: 'description', text: 'คำอธิบายกิจกรรม', align: 'left' },
      { value: 'lecturer_name', text: 'วิทยากร', align: 'center' },
      { value: "fullname", text: "ผู้สร้าง", align: "center" },
      { value: 'actions', text: '', sortable: false }
    ]
    return { headers: headers, data: [] }
  },

  async asyncData({ $axios, redirect }) {
    var user_id = parseInt(localStorage.getItem('user_id'))
    if (!user_id || user_id <= 0) {
      alert('โปรดเข้าสู่ระบบก่อน')
      redirect('/login')
      return
    }

    const results = await $axios.$get('/api/v1/activity/?is_published=true')

    // format data
    var index = 1
    var rows = results.map(function(row) {
      row.index = index++
      if (row.created_at)
        row.created_at = formatDateTimeText(row.created_at)
      if (row.userprofile_data && row.userprofile_data.fullname)
        row.fullname = row.userprofile_data.fullname
      console.log('row', row)
      return row
    })
    return { data: rows }
  },

  methods: {

    tableRow_Click(value) {
      //console.log(value);
      this.$router.push('/activity/' + value.id)
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

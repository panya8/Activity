<template>
  <div class='login-page mt-10 mb-10'>


    <v-layout flex align-center justify-center>
      <v-flex  xs6 sm6 elevation-5>
        <v-card>
          <!--                    <v-card-title class='teal accent-4 align-center'>-->
          <!--                      <h3>เข้าสู่ระบบ</h3>-->
          <!--                    </v-card-title>-->
          <v-card class='teal accent-4'>
            <h3 class='pt-4 pb-4 text-center'>เข้าสู่ระบบ</h3>
          </v-card>

          <v-card-text class='mt-2 ml-2'>
            <div>
              <v-form ref='form'>
                <v-text-field
                  v-model='user.username'
                  label='รหัสนิสิต/ชื่อผู้ใช้งาน'
                  counter
                  required
                ></v-text-field>
                <v-text-field
                  v-model='user.password'
                  label='รหัสผ่าน'
                  :append-icon="
                                      user.showPassword ? 'mdi-eye-off' : 'mdi-eye'
                                    "
                  :type="user.showPassword ? 'text' : 'password'"
                  required
                  @click:append='user.showPassword = !user.showPassword'
                ></v-text-field>
                <v-layout justify-center>
                  <v-btn :to="{path:'/register'}" class='mr-10 primary--text elevation-0' color='grey lighten-5'>
                    สมัครสมาชิก
                  </v-btn>
                  <v-btn @click='loginSubmit(user)' class='ml-10' color='primary'> เข้าสู่ระบบ</v-btn>
                </v-layout>
              </v-form>
            </div>
          </v-card-text>
        </v-card>
      </v-flex>
    </v-layout>
  </div>
  </v-container>

</template>

<script>
export default {
  data: function() {
    console.log('data', this.$auth)
    return {
      user: { username: '', password: '', showPassword: false }
    }
  },

  methods: {
    async loginSubmit(data) {

      try {
        var user_id = parseInt(localStorage.getItem('user_id'))
        if (user_id && user_id > 0) {
          window.location.href = '/activity'
          return
        }

        var results = await this.$auth.loginWith('local', { data: data })
        console.log('login', results)

        if (results.data && results.data.success) {

          var user = results.data.data
          //var user = await this.$axios.post('/api/v1/userdata/', results.data )
          //console.log('user', user);
          this.$auth.setUser(user)
          localStorage.setItem('user_id', user.id)
          localStorage.setItem('user', JSON.stringify(user))

          //console.log('method', this);
          //this.$router.go('/activity');
          window.location.href = '/activity'
        }

        //this.$auth.setUser( { data: data } );


        console.log('login successful')

      } catch (error) {
        alert('Cannot login. ')
        console.log('login unsuccessful', error)
      }
    }
  }
}
</script>
<style scoped>
.hero {
  background: url('../assets/1.jpg');
  background-size: cover;
  height: 100vh;
}
</style>

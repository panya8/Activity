<template>
    <div class="login-page">
        <v-layout flex align-center justify-center>
            <v-flex xs6 sm6 elevation-6>
                <v-card>
                  <v-card class='teal accent-4'>
                    <h2 class='pt-4 pb-4 text-center'>ออกจากระบบ</h2>
                  </v-card>

                    <v-card-text class="pt-4 text-center">
                        <h3 class='mt-5 mb-5 red--text'>ได้ทำการออกจากระบบแล้ว!</h3>
<!--                        <div>-->
<!--                            <v-btn @click="logout(user)" color="primary"> Back </v-btn>-->
<!--                        </div>-->
                    </v-card-text>
                </v-card>
            </v-flex>
        </v-layout>

    </div>
</template>

<script>
export default {
  data: function() {
      console.log('data', this.$auth );
      return {
          user: { username: '', password: '', showPassword: false },
      };
  },

  async asyncData( { $router } ) {
        try {

            localStorage.setItem('user', null);
            localStorage.setItem('user_id', null);

            alert('ได้ทำการออกจากระบบแล้ว.');

            window.location.href = '/login';


        } catch (error) {
            alert('Cannot logout. ' + error);
        }

  },

  methods: {
    async logout(data) {
        this.$router.go('/login');
    },
  },
}
</script>

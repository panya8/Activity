<template>
  <v-app>
    <v-app-bar dark clipped-left fixed app color='purple darken-4 no-print'>
      <v-avatar class='mr-2'>
        <v-img contain max-height='48' src='/senew.svg'></v-img>
      </v-avatar>
      <v-toolbar-title v-text='title' />
      <v-spacer />
      <v-btn text>หน้าหลัก</v-btn>
      <v-btn text :to="{path:'/activity'}">กิจกรรมสาขา</v-btn>
      <v-btn text>เกี่ยวกับสาขาวิชา</v-btn>
      <v-btn text>หลักสูตร</v-btn>
      <v-btn text>ติดต่อ</v-btn>
      <v-btn icon @click.stop='menuClick'>
        <v-icon>mdi-menu</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>


      <div v-if='login'>

        <!--แถบสีม่วง1-->
        <v-sheet color='purple darken-2 no-print' height='40'>
        </v-sheet>

        <!--แถบสีม่วง2 และ icon กิจกรรม-->
        <v-sheet align='center' color='purple darken-3 white--text no-print' height='120'>
          <v-avatar class='overview-box-icon close-right-40'
                    color='purple darken-3'
                    size='90'>
            <v-icon class='close-right-35' color='white' size='60'>
              mdi-calendar-search
            </v-icon>
          </v-avatar>
          <h2 class='mt-2 close-right-40'>ระบบกิจกรรม</h2>
        </v-sheet>

        <!--row menu & content-->
        <v-row>
          <v-col class='col-3 mt-5 no-print' md='2' lg='2' xl='3'>


            <v-card tile elevation='0'>

              <v-navigation-drawer

                permanent
              >
                <v-list>
                  <v-list-item v-if='user'>
                    <v-list-item-content>
                      <v-avatar>
                        <img
                          src='https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png'
                        >
                      </v-avatar>

                      <v-list-item-title class='text-h6 text-center'>
                        <br /> {{ fullname }}
                      </v-list-item-title>
                      <v-list-item-subtitle class='text-h8 text-center'>
                        ({{ profile_type }})
                      </v-list-item-subtitle>
                    </v-list-item-content>
                  </v-list-item>

                  <v-list-item-group color='primary'>

                    <v-list-item :to="{path:'/activity'}" exact>
                      <v-list-item-icon>
                        <v-icon>mdi-bell-ring
                        </v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>กิจกรรมล่าสุด</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>


                    <v-list-item :to="{path:'/activity/all'}">
                      <v-list-item-icon>
                        <v-icon>mdi-view-dashboard
                        </v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>สรุปกิจกรรมทั้งหมด</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

                    <v-list-item :to="{path:'/activity/my'}" v-if='is_logged'>
                      <v-list-item-icon>
                        <v-icon>mdi-calendar-edit
                        </v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>กิจกรรมของฉัน</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

<!--                    <v-list-item :to="{path:'/activity/edit/0'}" v-if='is_logged'>-->
<!--                      <v-list-item-icon>-->
<!--                        <v-icon>mdi-calendar-plus-->
<!--                        </v-icon>-->
<!--                      </v-list-item-icon>-->
<!--                      <v-list-item-content>-->
<!--                        <v-list-item-title>สร้างกิจกรรม</v-list-item-title>-->
<!--                      </v-list-item-content>-->
<!--                    </v-list-item>-->

<!--                    <v-list-item :to="{path:'/users/'}" v-if='is_logged'>-->
<!--                      <v-list-item-icon>-->
<!--                        <v-icon>mdi-account-->
<!--                        </v-icon>-->
<!--                      </v-list-item-icon>-->
<!--                      <v-list-item-content>-->
<!--                        <v-list-item-title>สมาชิก</v-list-item-title>-->
<!--                      </v-list-item-content>-->
<!--                    </v-list-item>-->

<!--                    <v-list-item :to="{path:'/users/edit/0'}" v-if='is_logged'>-->
<!--                      <v-list-item-icon>-->
<!--                        <v-icon>mdi-account-plus-->
<!--                        </v-icon>-->
<!--                      </v-list-item-icon>-->
<!--                      <v-list-item-content>-->
<!--                        <v-list-item-title>สร้างสมาชิก</v-list-item-title>-->
<!--                      </v-list-item-content>-->
<!--                    </v-list-item>-->

                    <v-divider></v-divider>

                    <v-list-item :to="{path:'/logout'}" v-if='is_logged'>
                      <v-list-item-icon>
                        <v-icon>mdi-logout
                        </v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>ออกจากระบบ</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>

                    <v-list-item :to="{path:'/login'}" v-if='!is_logged'>
                      <v-list-item-icon>
                        <v-icon>mdi-login
                        </v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>เข้าสู่ระบบ</v-list-item-title>
                      </v-list-item-content>
                    </v-list-item>
                    <!--                    </v-list-item-group>-->
                    <!--                      <v-list-item :to="{path:'/register'}" v-if="!is_logged">-->
                    <!--                        <v-list-item-icon>-->
                    <!--                          <v-icon>mdi-account-edit-->
                    <!--                          </v-icon>-->
                    <!--                        </v-list-item-icon>-->
                    <!--                        <v-list-item-content>-->
                    <!--                          <v-list-item-title>ลงทะเบียนสมาชิก</v-list-item-title>-->
                    <!--                        </v-list-item-content>-->
                    <!--                      </v-list-item>-->
                  </v-list-item-group>
                </v-list>

              </v-navigation-drawer>
            </v-card>
          </v-col>
          <v-col cols='7' class='mt-10 justify-center' >
            <nuxt class='justify-center' />
          </v-col>
        </v-row>
      </div>

    </v-main>

    <v-footer color='no-print'
      :absolute='!fixed'
      app
    >
      <span>&copy; {{ new Date().getFullYear() }}</span>
    </v-footer>
  </v-app>
</template>

<script>
export default {
  data() {
    var user_id = parseInt(localStorage.getItem('user_id'))
    var profile_type = 'guest'
    var fullname = ''
    var userprofile = null
    var is_logged = false
    if (user_id && user_id > 0) {
      userprofile = JSON.parse(localStorage.getItem('user'))

      if (userprofile.id == user_id) {
        fullname = userprofile.fullname
        profile_type = (userprofile.profile_type == 'teacher') ? 'อาจารย์' : 'สมาชิก'
        is_logged = true
      } else {
        userprofile = null
      }
    }

    return {
      login: true,
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Welcome',
          to: '/'
        },
        {
          icon: 'mdi-chart-bubble',
          title: 'Inspire',
          to: '/inspire'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Software Engineering',
      is_logged: is_logged,
      fullname: fullname,
      profile_type: profile_type,
      user: userprofile

    }
  }


}
</script>

<style scoped>
.overview-box-icon {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  line-height: 40px;
  margin: 0 auto;
  margin-top: -35px;
}
.close-right-40 {
  margin-right: -40px;
}
.close-right-35 {
  margin-right: -5px;
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

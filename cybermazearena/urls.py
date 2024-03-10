"""
URL configuration for cybermazearena project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from mainapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.loading),
    path('login/', views.signIn, name='login'),
    path('postsignIn/', views.postsignIn),
    path('signup/', views.signUp, name="signup"),
    path('logout/', views.logout, name="log"),
    path('profile/', views.profile, name="profile"),
    path('postsignUp', views.postsignUp),
    path('reset/', views.reset),
    path('postReset/', views.postReset),
    path('main/', views.mainpage, name="main"),
    path('blogs/', views.blog_view, name='blogs'),
    path('blog/howtoapproach/', views.hta_view, name="howtoapproach"),
    path('blog/crypto/', views.crypto_view, name='crypto'),
    path('blog/forensics/', views.forensics_view, name='forensics'),
    path('blog/pwn/', views.pwn_view, name='pwn'),
    path('blog/reversing/', views.reversing_view, name='reversing'),
    path('blog/osint/', views.osint_view, name='osint'),
    path('blog/stegano/', views.stegano_view, name='stegano'),
    path('blog/web/', views.web_view, name='web'),
    path('blog/gitlab2023/', views.gitlab_view, name="gitlab2023"),
    path('blog/chrome0day/', views.chrome_view, name="chrome0day"),
    path('learn/', views.learn_view, name='learn'),
    path('learn/guided/', views.guided_view, name='guided'),
    path('learn/practice/', views.practice_view, name='practice'),
    path('verify_flag/', views.verify_flag, name='verify_flag')
]

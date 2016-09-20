using System;
using Android.Text;
using Android.Content;
using Android.Runtime;
using Android.Views;
using Android.App;
using Android.Widget;
using Android.OS;

namespace App1
{
    [Activity(Label = "App1", MainLauncher = true, Icon = "@drawable/icon")]
    public class MainActivity : Activity
    {
        protected override void OnCreate(Bundle bundle)
        {
            int count = 1;

            base.OnCreate(bundle);

            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.Main);

            Button myButton = FindViewById<Button>(Resource.Id.myButton);

            myButton.Click += delegate
            {
                myButton.Text = string.Format("{0} clicks!", count++);
            };

            Button btn1 = FindViewById<Button>(Resource.Id.btn2);

            btn1.Click += delegate
            {
                StartActivity(typeof(Activ2));
            };
        }
    }
}


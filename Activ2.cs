using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using Android.App;
using Android.Content;
using Android.OS;
using Android.Runtime;
using Android.Views;
using Android.Widget;

namespace App1
{
    [Activity(Label = "Activ2")]
    public class Activ2 : Activity
    {
        int count2 = 1;

        protected override void OnCreate(Bundle bundle)
        {
            base.OnCreate(bundle);

            // Create your application here
            SetContentView(Resource.Layout.layout2);

            EditText elseText = FindViewById<EditText>(Resource.Id.elseText);
            Button button2 = FindViewById<Button>(Resource.Id.button2);

            button2.Click += delegate
            {
                button2.Text = string.Format("{0} clicks!", count2++);
            };
        }
    }
}
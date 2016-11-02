//This is the home view. Mainlauncher is set to this page so this is what loads when the app starts.
//This just has 2 buttons, one for quick search, one for recipes. When you click one of the buttons, it starts the desired activity.

using System;
using Android.Views;
using Android.Content;
using Android.Runtime;
using Android.App;
using Android.Widget;
using Android.OS;
using Android.Content.Res;
using System.IO;
using SQLite;
using System.Linq;
using Android.Database.Sqlite;
using System.Collections.Generic;
using System.Collections;

namespace nutr_grabber
{
    [Activity(Label = "Home", MainLauncher = true, Icon = "@drawable/icon")]
    public class Home : Activity
    {
        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            //sets the view
            SetContentView(Resource.Layout.HomeView);

            // sets the buttons
            Button quickBtn = FindViewById<Button>(Resource.Id.quickSearchBtn);
            Button recipeBtn = FindViewById<Button>(Resource.Id.recipeSearchBtn);



            quickBtn.Click += (object sender, EventArgs e) =>
            {
                StartActivity(typeof(QuickSearch));
            };

            recipeBtn.Click += (object sender, EventArgs e) =>
            {
                StartActivity(typeof(RecipeActivity));
            };
        }
    }
}

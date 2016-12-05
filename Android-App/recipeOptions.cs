//after submitting a recipe, gives the options of viewing the nutrients or calories

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

namespace NutriApp
{
    [Activity(Label = "recipeOptions")]
    public class recipeOptions : Activity
    {


        public List<string> ingredList;

        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            //sets the view
            SetContentView(Resource.Layout.recipeOptions);

            // sets the buttons
            Button ntrBtn = FindViewById<Button>(Resource.Id.ntrBtn);
            Button ingBtn = FindViewById<Button>(Resource.Id.ingBtn);

            base.OnCreate(savedInstanceState);

            var rName = Intent.GetStringExtra("rName") ?? "No data";
            var Kcal = Intent.GetStringExtra("Kcal") ?? "No data";
            var protein = Intent.GetStringExtra("protein") ?? "No data";
            var fat = Intent.GetStringExtra("fat") ?? "No data";
            var carbs = Intent.GetStringExtra("carbs") ?? "No data";
            var sodium = Intent.GetStringExtra("sodium") ?? "No data";
            var chol = Intent.GetStringExtra("chol") ?? "No data";
            var sugar = Intent.GetStringExtra("sugar") ?? "No data";

            ingredList = new List<string>();

            ntrBtn.Click += (object sender, EventArgs e) =>
            {


                var third = new Intent(this, typeof(nReList));
                // passes items to second activity, then launches the new activity
                third.PutExtra("rName", Convert.ToString(rName));
                third.PutExtra("Kcal", Convert.ToString(Kcal));
                third.PutExtra("protein", Convert.ToString(protein));
                third.PutExtra("fat", Convert.ToString(fat));
                third.PutExtra("carbs", Convert.ToString(carbs));
                third.PutExtra("sodium", Convert.ToString(sodium));
                third.PutExtra("chol", Convert.ToString(chol));
                third.PutExtra("sugar", Convert.ToString(sugar));

                StartActivity(third);
            };

            ingBtn.Click += (object sender, EventArgs e) =>
            {
                StartActivity(typeof(iReList));
            };
        }
    }
}

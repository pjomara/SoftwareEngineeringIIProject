// this is used to create a nutrient display list. this is specifiallcy for the RecipeActivity so it is properly formatted


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

namespace NutriApp
{
    [Activity(Label = "")]
    public class nReList : Activity
    {
        private List<string> nutrs;
        private ListView nListView;

        protected override void OnCreate(Bundle savedInstanceState)
        {

            SetContentView(Resource.Layout.nutrientRecipeList);
            nListView = FindViewById<ListView>(Resource.Id.nutRecListView);

            base.OnCreate(savedInstanceState);
            var rName = Intent.GetStringExtra("rName") ?? "No data";
            var Kcal = Intent.GetStringExtra("Kcal") ?? "No data";
            var protein = Intent.GetStringExtra("protein") ?? "No data";
            var fat = Intent.GetStringExtra("fat") ?? "No data";
            var carbs = Intent.GetStringExtra("carbs") ?? "No data";
            var sodium = Intent.GetStringExtra("sodium") ?? "No data";
            var chol = Intent.GetStringExtra("chol") ?? "No data";
            var sugar = Intent.GetStringExtra("sugar") ?? "No data";


            //make new list for listview to use, adds all of the passed data to the list
            nutrs = new List<string>();
            nutrs.Add(rName);
            nutrs.Add("Calories: " + Kcal);
            nutrs.Add("Protein: " + protein + "g");
            nutrs.Add("Fat: " + fat + "g");
            nutrs.Add("Carbs: " + carbs + "g");
            nutrs.Add("Sodium: " + sodium + "mg");
            nutrs.Add("Cholesterol: " + chol + "mg");
            nutrs.Add("Sugar: " + sugar + "g");

            ArrayAdapter<string> adapter = new ArrayAdapter<string>(this, Android.Resource.Layout.SimpleListItem1, nutrs);
            nListView.Adapter = adapter;

        }
    }
}

//just added some documentation

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
    [Activity(Label = "ListDisplay")]
    public class ListDisplay : MainActivity
    {
        private List<string> nutrs;
        private ListView nListView;

        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            //set view as list view
            SetContentView(Resource.Layout.nutrList);
            nListView = FindViewById <ListView>(Resource.Id.nutrListView);

            // receive nutrients from main activity and store them
            var name = Intent.GetStringExtra("name") ?? "No data";
            var Kcal = Intent.GetStringExtra("Kcal") ?? "No data";
            var protein = Intent.GetStringExtra("protein") ?? "No data";
            var fat = Intent.GetStringExtra("fat") ?? "No data";
            var carbs = Intent.GetStringExtra("carbs") ?? "No data";
            var sodium = Intent.GetStringExtra("sodium") ?? "No data";
            var sugar = Intent.GetStringExtra("sugar") ?? "No data";
            var num = Intent.GetStringExtra("num") ?? "No data";
            var unit = Intent.GetStringExtra("unit") ?? "No data";

            //make new list for listview to use, adds all of the passed data to the list
            nutrs = new List<string>();
            nutrs.Add(num + " " + unit + " of " + name);
            nutrs.Add("Calories: " + Kcal);
            nutrs.Add("Protein: " + protein + "g");
            nutrs.Add("Fat: " + fat + "g");
            nutrs.Add("Carbs: " + carbs + "g");
            nutrs.Add("Sodium: " + sodium + "mg");
            nutrs.Add("Sugar: " + sugar + "g");

            ArrayAdapter<string> adapter = new ArrayAdapter<string>(this, Android.Resource.Layout.SimpleListItem1, nutrs);
            nListView.Adapter = adapter;

        }
    }
}

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

            SetContentView(Resource.Layout.nutrList);
            nListView = FindViewById < ListView>(Resource.Id.nutrListView);


            var name = Intent.GetStringExtra("name") ?? "No data";
            var Kcal = Intent.GetStringExtra("Kcal") ?? "No data";
            var protein = Intent.GetStringExtra("protein") ?? "No data";
            var fat = Intent.GetStringExtra("fat") ?? "No data";
            var carbs = Intent.GetStringExtra("carbs") ?? "No data";
            var sodium = Intent.GetStringExtra("sodium") ?? "No data";
            var sugar = Intent.GetStringExtra("sugar") ?? "No data";

            nutrs = new List<string>();
            nutrs.Add(name);
            nutrs.Add("Caloris: " + Kcal);
            nutrs.Add("Protein: " + protein);
            nutrs.Add("Fat: " + fat);
            nutrs.Add("Carbs: " + carbs);
            nutrs.Add("Sodium: " + sodium);
            nutrs.Add("Sugar: " + sugar);

            ArrayAdapter<string> adapter = new ArrayAdapter<string>(this, Android.Resource.Layout.SimpleListItem1, nutrs);

            nListView.Adapter = adapter;

        }
    }
}
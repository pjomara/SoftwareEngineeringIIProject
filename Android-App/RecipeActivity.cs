// added a makeToast message instead of an alert dialog; user doesnt need to click on screen --> faster
//Array list for ingredients is declared as a static so I don't need to pass the items individually and can just be accessed by the necessary activity


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
    [Activity(Label = "Recipe")]
    public class RecipeActivity : Activity
    {
        string str1;
        string unitEntered;
        double tspInCup = 48.0;
        double tbspInCup = 16.0;
        double tspInTbsp = 3.0;
        double ozInCup = 8.0;
        double ozInTbsp = 0.5;
        double ozInLb = 16.0;

        double amountEntered;

        string name;
        string rName;
        double cal;
        double protein;
        double fat;
        double carbs;
        double sodium;
        double chol;
        double sugar;
        double num;
        string unit;

        double totCal;
        double totProtein;
        double totFat;
        double totCarbs;
        double totSodium;
        double totChol;
        double totSugar;

        public static List<string> ingredList;
        

        // Android needs a database to be copied from assets to a useable location in inernal memory
        public void copyDataBase()
        {
            var dbPath = System.IO.Path.Combine(System.Environment.GetFolderPath(System.Environment.SpecialFolder.Personal), "USDADataProto.db");

            if (!System.IO.File.Exists(dbPath))
            {
                var dbAssetStream = Assets.Open("USDADataProto.db");
                var dbFileStream = new FileStream(dbPath, FileMode.OpenOrCreate);
                var buffer = new byte[1024];

                int b = buffer.Length;
                int length;

                while ((length = dbAssetStream.Read(buffer, 0, b)) > 0)
                {
                    dbFileStream.Write(buffer, 0, length);
                }

                dbFileStream.Flush();
                dbFileStream.Close();
                dbAssetStream.Close();
            }
        }

        // gets item from spinner
        private void unitSpin_ItemSelected(object sender, AdapterView.ItemSelectedEventArgs e)
        {
            Spinner spinner = (Spinner)sender;
            unitEntered = string.Format("{0}", spinner.GetItemAtPosition(e.Position));

        }

        protected override void OnCreate(Bundle bundle)
        {
            base.OnCreate(bundle);

            //create the database copy
            copyDataBase();


            // Set view from the main layout resource
            SetContentView(Resource.Layout.RecipeLayout);


            //set widgets
            TextView message = FindViewById<TextView>(Resource.Id.textAmount);
            EditText amount = FindViewById<EditText>(Resource.Id.enterAmount);
            TextView message3 = FindViewById<TextView>(Resource.Id.textUnit);
            Spinner unitSpin = FindViewById<Spinner>(Resource.Id.unitSpinner);
            TextView message2 = FindViewById<TextView>(Resource.Id.textIngred);
            AutoCompleteTextView autoIngred = FindViewById<AutoCompleteTextView>(Resource.Id.autoCompIngred);
            Button add = FindViewById<Button>(Resource.Id.addIngred);
            Button done = FindViewById<Button>(Resource.Id.finalize);
            TextView message4 = FindViewById<TextView>(Resource.Id.recipeName);
            EditText recipeName = FindViewById<EditText>(Resource.Id.enterName);
            Button submit = FindViewById<Button>(Resource.Id.submit);

            message4.Enabled = false;
            recipeName.Enabled = false;
            submit.Enabled = false;

            ingredList = new List<string>();

            //open sqlite connection, create table
            var Path = System.IO.Path.Combine(System.Environment.GetFolderPath(System.Environment.SpecialFolder.Personal), "USDADataProto.db");
            var db = new SQLiteConnection(Path);
            db.CreateTable<USDADataProto>();

            // creates a spinner that gets populated with items from my resource
            var adapter = ArrayAdapter.CreateFromResource(
                   this, Resource.Array.units_array, Android.Resource.Layout.SimpleSpinnerItem);
            adapter.SetDropDownViewResource(Android.Resource.Layout.SimpleSpinnerDropDownItem);
            unitSpin.Adapter = adapter;

            // get the selected unit from spinner
            unitSpin.ItemSelected += new EventHandler<AdapterView.ItemSelectedEventArgs>(unitSpin_ItemSelected);



            //this is used to create the actual auto-text.
            //I create a new, blank array. Then select the entire table I created earlier.
            //Then, for every row of info add only the Shrt_Desc (the name of the ingredient)
            // to the blank array. 
            ArrayList autoIngs = new ArrayList();
            var addToAuto = db.Table<USDADataProto>();
            foreach (var auto in addToAuto)
            {
                autoIngs.Add(auto.Shrt_Desc);
            }
            
            //When the text in the text-box changes, populate the auto-complete suggestions 
            // with the name of the ingredients from the array
            autoIngred.TextChanged += delegate
            {
                ArrayAdapter autoCompAdapter = new ArrayAdapter(this, Android.Resource.Layout.SimpleDropDownItem1Line, autoIngs);
                autoIngred.Adapter = autoCompAdapter;
            };




            //when you click the add button
            add.Click += (object sender, EventArgs e) =>
            {
                //formats input text. TrimEnd takes the space off the end.
                //If the space is there it causes a crash. The datbase is also all caps.
                str1 = autoIngred.Text;
                str1 = str1.TrimEnd();
                str1 = str1.ToUpper();
                
                //converts form string to double for math operations
                amountEntered = Convert.ToDouble(amount.Text);


                // make list from a query in the USDADataProto table. Selects everything in the row where shrt_desc is equal to str1
                List<USDADataProto> query = db.Query<USDADataProto>("SELECT * FROM USDADataProto WHERE Shrt_Desc = ?", str1);

                foreach (var i in query)
                {
                    name = i.Shrt_Desc;
                    cal = i.Energ_Kcal;
                    protein = i.Protein_g;
                    fat = i.Lipid_Tot_g;
                    carbs = i.Carbohydrt_g;
                    sodium = i.Sodium_mg;
                    chol = i.Cholestrl_mg;
                    sugar = i.Sugar_Tot_g;
                    num = i.num;
                    unit = i.unit;
                }

                //nutrient numbers get divded by the amount in the db
                //put everything at a base level of 1
                cal = cal / num;
                protein = protein / num;
                fat = fat / num;
                carbs = carbs / num;
                sodium = sodium / num;
                chol = chol / num;
                sugar = sugar / num;

                //unit conversions
                if (unit == unitEntered)
                {
                    cal = cal * amountEntered;
                    protein = protein * amountEntered;
                    fat = fat * amountEntered;
                    carbs = carbs * amountEntered;
                    sodium = sodium * amountEntered;
                    chol = chol * amountEntered;
                    sugar = sugar * amountEntered;
                }
                else if (unit == "cup" && unitEntered == "tbsp")
                {
                    cal = (cal / tbspInCup) * amountEntered;
                    protein = (protein / tbspInCup) * amountEntered;
                    fat = (fat / tbspInCup) * amountEntered;
                    carbs = (carbs / tbspInCup) * amountEntered;
                    sodium = (sodium / tbspInCup) * amountEntered;
                    chol = (chol / tbspInCup) * amountEntered;
                    sugar = (sugar / tbspInCup) * amountEntered;
                }
                else if (unit == "cup" && unitEntered == "tsp")
                {
                    cal = (cal / tspInCup) * amountEntered;
                    protein = (protein / tspInCup) * amountEntered;
                    fat = (fat / tspInCup) * amountEntered;
                    carbs = (carbs / tspInCup) * amountEntered;
                    sodium = (sodium / tspInCup) * amountEntered;
                    chol = (chol / tspInCup) * amountEntered;
                    sugar = (sugar / tspInCup) * amountEntered;
                }
                else if (unit == "tsp" && unitEntered == "cup")
                {
                    cal = (cal * tspInCup) * amountEntered;
                    protein = (protein * tspInCup) * amountEntered;
                    fat = (fat * tspInCup) * amountEntered;
                    carbs = (carbs * tspInCup) * amountEntered;
                    sodium = (sodium * tspInCup) * amountEntered;
                    chol = (chol * tspInCup) * amountEntered;
                    sugar = (sugar * tspInCup) * amountEntered;
                }
                else if (unit == "tsp" && unitEntered == "tbsp")
                {
                    cal = (cal * tspInTbsp) * amountEntered;
                    protein = (protein * tspInTbsp) * amountEntered;
                    fat = (fat * tspInTbsp) * amountEntered;
                    carbs = (carbs * tspInTbsp) * amountEntered;
                    sodium = (sodium * tspInTbsp) * amountEntered;
                    chol = (chol * tspInTbsp) * amountEntered;
                    sugar = (sugar * tspInTbsp) * amountEntered;
                }
                else if (unit == "tbsp" && unitEntered == "cup")
                {
                    cal = (cal * tbspInCup) * amountEntered;
                    protein = (protein * tbspInCup) * amountEntered;
                    fat = (fat * tbspInCup) * amountEntered;
                    carbs = (carbs * tbspInCup) * amountEntered;
                    sodium = (sodium * tbspInCup) * amountEntered;
                    chol = (chol * tbspInCup) * amountEntered;
                    sugar = (sugar * tbspInCup) * amountEntered;
                }
                else if (unit == "tbsp" && unitEntered == "tsp")
                {
                    cal = (cal / tspInTbsp) * amountEntered;
                    protein = (protein / tspInTbsp) * amountEntered;
                    fat = (fat / tspInTbsp) * amountEntered;
                    carbs = (carbs / tspInTbsp) * amountEntered;
                    sodium = (sodium / tspInTbsp) * amountEntered;
                    chol = (chol / tspInTbsp) * amountEntered;
                    sugar = (sugar / tspInTbsp) * amountEntered;
                }
                else if (unit == "oz" && unitEntered == "tbsp")
                {
                    cal = (cal / ozInTbsp) * amountEntered;
                    protein = (protein / ozInTbsp) * amountEntered;
                    fat = (fat / ozInTbsp) * amountEntered;
                    carbs = (carbs / ozInTbsp) * amountEntered;
                    sodium = (sodium / ozInTbsp) * amountEntered;
                    chol = (chol / ozInTbsp) * amountEntered;
                    sugar = (sugar / ozInTbsp) * amountEntered;
                }
                else if (unit == "oz" && unitEntered == "cup")
                {
                    cal = (cal * ozInCup) * amountEntered;
                    protein = (protein * ozInCup) * amountEntered;
                    fat = (fat * ozInCup) * amountEntered;
                    carbs = (carbs * ozInCup) * amountEntered;
                    sodium = (sodium * ozInCup) * amountEntered;
                    chol = (chol * ozInCup) * amountEntered;
                    sugar = (sugar * ozInCup) * amountEntered;
                }
                else if (unit == "tbsp" && unitEntered == "oz")
                {
                    cal = (cal * ozInTbsp) * amountEntered;
                    protein = (protein * ozInTbsp) * amountEntered;
                    fat = (fat * ozInTbsp) * amountEntered;
                    carbs = (carbs * ozInTbsp) * amountEntered;
                    sodium = (sodium * ozInTbsp) * amountEntered;
                    chol = (chol * ozInTbsp) * amountEntered;
                    sugar = (sugar * ozInTbsp) * amountEntered;
                }
                else if (unit == "cup" && unitEntered == "oz")
                {
                    cal = (cal / ozInTbsp) * amountEntered;
                    protein = (protein / ozInTbsp) * amountEntered;
                    fat = (fat / ozInTbsp) * amountEntered;
                    carbs = (carbs / ozInTbsp) * amountEntered;
                    sodium = (sodium / ozInTbsp) * amountEntered;
                    chol = (chol / ozInTbsp) * amountEntered;
                    sugar = (sugar / ozInTbsp) * amountEntered;
                }
                else if (unit == "oz" && unitEntered == "lb")
                {
                    cal = (cal * ozInLb) * amountEntered;
                    protein = (protein * ozInLb) * amountEntered;
                    fat = (fat * ozInLb) * amountEntered;
                    carbs = (carbs * ozInLb) * amountEntered;
                    sodium = (sodium * ozInLb) * amountEntered;
                    chol = (chol * ozInLb) * amountEntered;
                    sugar = (sugar * ozInLb) * amountEntered;
                }
                else if (unit == "lb" && unitEntered == "oz")
                {
                    cal = (cal / ozInLb) * amountEntered;
                    protein = (protein / ozInLb) * amountEntered;
                    fat = (fat / ozInLb) * amountEntered;
                    carbs = (carbs / ozInLb) * amountEntered;
                    sodium = (sodium / ozInLb) * amountEntered;
                    chol = (chol / ozInLb) * amountEntered;
                    sugar = (sugar / ozInLb) * amountEntered;
                }


                // formats doubles to 2 decimal places
                cal = Math.Round(cal, 2);
                protein = Math.Round(protein, 2);
                fat = Math.Round(fat, 2);
                carbs = Math.Round(carbs, 2);
                sodium = Math.Round(sodium, 2);
                chol = Math.Round(chol, 2);
                sugar = Math.Round(sugar, 2);

                //keeps track of total amounts
                totCal = totCal + cal;
                totProtein = totProtein + protein;
                totFat = totFat + fat;
                totCarbs = totCarbs + carbs;
                totSodium = totSodium + sodium;
                totChol = totChol + chol;
                totSugar = totSugar + sugar;

                //reformats text boxes to blank (so user doesn't have to manually backspace everything)
                amount.Text = "";
                autoIngred.Text = "";


                ingredList.Add(amountEntered + " " + unitEntered + " of " + name);

                //gives user a message to let them know it was succesfully added
                string toastMessage = amountEntered + " " + unitEntered + "/s of " + name + " added to recipe";
                Toast.MakeText(this, toastMessage, ToastLength.Short).Show();

            };

            done.Click += (object sender, EventArgs e) =>
            {
                message4.Enabled = true;
                recipeName.Enabled = true;
                submit.Enabled = true;

            };

            submit.Click += (object sender, EventArgs e) =>
            {
                rName = recipeName.Text;
                // sets the intent to pass the info to listdisplay activity
                var second = new Intent(this, typeof(recipeOptions));
                // passes items to second activity, then launches the new activity
                second.PutExtra("rName", Convert.ToString(rName));
                second.PutExtra("Kcal", Convert.ToString(totCal));
                second.PutExtra("protein", Convert.ToString(totProtein));
                second.PutExtra("fat", Convert.ToString(totFat));
                second.PutExtra("carbs", Convert.ToString(totCarbs));
                second.PutExtra("sodium", Convert.ToString(totSodium));
                second.PutExtra("chol", Convert.ToString(totChol));
                second.PutExtra("sugar", Convert.ToString(totSugar));

                StartActivity(second);
            };


        }



        //---------------------------------------------------------------------------------

        public class USDADataProto
        {

            public int NDB_No { get; set; }
            [PrimaryKey]
            public string Shrt_Desc { get; set; }
            public float Energ_Kcal { get; set; }
            public float Protein_g { get; set; }
            public float Lipid_Tot_g { get; set; }
            public float Ash_g { get; set; }
            public float Carbohydrt_g { get; set; }
            public float Fiber_TD_g { get; set; }
            public float Sugar_Tot_g { get; set; }
            public float Calcium_mg { get; set; }
            public float Iron_mg { get; set; }
            public float Magnesium_mg { get; set; }
            public float Phosphorus_mg { get; set; }
            public float Potassium_mg { get; set; }
            public float Sodium_mg { get; set; }
            public float Zinc_mg { get; set; }
            public float Copper_mg { get; set; }
            public float Manganese_mg { get; set; }
            public float Selenium_ug { get; set; }
            public float Vit_C_mg { get; set; }
            public float Thiamin_mg { get; set; }
            public float Riboflavin_mg { get; set; }
            public float Niacin_mg { get; set; }
            public float Panto_Acid_mg { get; set; }
            public float Vit_B6_mg { get; set; }
            public float Folate_Tot_ug { get; set; }
            public float Folic_Acid_ug { get; set; }
            public float Food_Folate_ug { get; set; }
            public float Folate_DFE_ug { get; set; }
            public float Choline_Tot_mg { get; set; }
            public float Vit_B12_ug { get; set; }
            public float Vit_A_IU { get; set; }
            public float Vit_A_RAE { get; set; }
            public float Retinol_ug { get; set; }
            public float Alpha_Carot_ug { get; set; }
            public float Beta_Carot_ug { get; set; }
            public float Beta_Crypt_ug { get; set; }
            public float Lycopene_ug { get; set; }
            public float Lut_Zea_ug { get; set; }
            public float Vit_E_mg { get; set; }
            public float Vit_D_ug { get; set; }
            public float Vit_D_IU { get; set; }
            public float Vit_K_ug { get; set; }
            public float FA_Sat_g { get; set; }
            public float FA_Mono_g { get; set; }
            public float FA_Poly_g { get; set; }
            public float Cholestrl_mg { get; set; }
            public float Gm_unit { get; set; }
            public float num { get; set; }
            public string unit { get; set; }

        }

    }
}

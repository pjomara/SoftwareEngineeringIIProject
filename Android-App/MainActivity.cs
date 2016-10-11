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

    [Activity(Label = "nutr_grabber", MainLauncher = true, Icon = "@drawable/icon")]
    public class MainActivity : Activity
    {
                string str1;
        
                // Android needs a databse to be copied from assets to a useable location
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


        protected override void OnCreate(Bundle bundle)
        {
            base.OnCreate(bundle);
            
            //create the database copy
            copyDataBase();
            

            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.Main);


            //set widgets
            TextView message = FindViewById<TextView>(Resource.Id.message);
            EditText ingred = FindViewById<EditText>(Resource.Id.enterHere);
            Button search = FindViewById<Button>(Resource.Id.search);

            //open sqlite connection, create table
            var Path = System.IO.Path.Combine(System.Environment.GetFolderPath(System.Environment.SpecialFolder.Personal), "USDADataProto.db");
            var db = new SQLiteConnection(Path);
            db.CreateTable<USDADataProto>();

            
            //when you click the search button
                search.Click += (object sender, EventArgs e) =>
                    {
                        str1 = ingred.Text;
                        str1 = str1.TrimEnd();
                        str1 = str1.ToUpper();
                        

                        // make list from a query in the USDADataProto table. Selects evertyihg in the row where shrt_desc is equal to str1
                        List<USDADataProto> query = db.Query<USDADataProto>("SELECT * FROM USDADataProto WHERE Shrt_Desc = ?", str1);

                        var second = new Intent(this, typeof(ListDisplay));
                        
                        
                        foreach (var item in query)
                        {
                            /*
                            new AlertDialog.Builder(this)
                                    .SetMessage("Calories:  " + item.Energ_Kcal + " per "  + item.num + " " + Convert.ToString(item.unit))                       
                                    .Show();*/
                                  
                            second.PutExtra("name", Convert.ToString(item.Shrt_Desc));
                            second.PutExtra("Kcal", Convert.ToString(item.Energ_Kcal));
                            second.PutExtra("protein", Convert.ToString(item.Protein_g));
                            second.PutExtra("fat", Convert.ToString(item.Lipid_Tot_g));
                            second.PutExtra("carbs", Convert.ToString(item.Carbohydrt_g));
                            second.PutExtra("sodium", Convert.ToString(item.Sodium_mg));
                            second.PutExtra("sugar", Convert.ToString(item.Sugar_Tot_g));                   
                            StartActivity(second);
                            
                        }
                    };
        }



//----------------------------------------------------------------------------
       
        public class USDADataProto
        {
           
            public int NDB_No { get; set; }
            [PrimaryKey]
            public string Shrt_Desc { get; set; }
            public int Energ_Kcal { get; set; }           
            public int Protein_g { get; set; }
            public int Lipid_Tot_g { get; set; }
            public int Ash_g { get; set; }
            public int Carbohydrt_g { get; set; }
            public int Fiber_TD_g { get; set; }
            public int Sugar_Tot_g { get; set; }
            public int Calcium_mg { get; set; }
            public int Iron_mg { get; set; }
            public int Magnesium_mg { get; set; }
            public int Phosphorus_mg { get; set; }
            public int Potassium_mg { get; set; }
            public int Sodium_mg { get; set; }
            public int Zinc_mg { get; set; }
            public int Copper_mg { get; set; }
            public int Manganese_mg { get; set; }
            public int Selenium_ug { get; set; }
            public int Vit_C_mg { get; set; }
            public int Thiamin_mg { get; set; }
            public int Riboflavin_mg { get; set; }
            public int Niacin_mg { get; set; }
            public int Panto_Acid_mg { get; set; }
            public int Vit_B6_mg { get; set; }
            public int Folate_Tot_ug { get; set; }
            public int Folic_Acid_ug { get; set; }
            public int Food_Folate_ug { get; set; }
            public int Folate_DFE_ug { get; set; }
            public int Choline_Tot_mg { get; set; }
            public int Vit_B12_ug { get; set; }
            public int Vit_A_IU { get; set; }
            public int Vit_A_RAE { get; set; }
            public int Retinol_ug { get; set; }
            public int Alpha_Carot_ug { get; set; }
            public int Beta_Carot_ug { get; set; }
            public int Beta_Crypt_ug { get; set; }
            public int Lycopene_ug { get; set; }
            public int Lut_Zea_ug { get; set; }
            public int Vit_E_mg { get; set; }
            public int Vit_D_ug { get; set; }
            public int Vit_D_IU { get; set; }
            public int Vit_K_ug { get; set; }
            public int FA_Sat_g { get; set; }
            public int FA_Mono_g { get; set; }
            public int FA_Poly_g { get; set; }
            public int Cholestrl_mg { get; set; }
            public int Gm_unit { get; set; }
            public int num { get; set; }
            public int unit { get; set; }

    
        }




    }
}

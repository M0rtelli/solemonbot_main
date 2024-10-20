import app.base as base

localMarketPlaceAllAd = []
localUsers = []

def loadMarketPlaceAllAd():
    count = 0


    for row in base.cursor.execute(f"SELECT * FROM marketplace"):
            localMarketPlaceAllAd.insert(len(localMarketPlaceAllAd), {
                  "id":row[0],
                  "uid":row[1],
                  "name":row[2],
                  "status":row[3],
                  "price":row[4],
                  "photo_id":row[5],
                  "comment":row[6]
            })
            count += 1

    print(f"[LocalData]: Loaded {count} Marketplace AD!")

    # print(localMarketPlaceAllAd[1]["name"])
            
def LoadUsers():
      count = 0

      for row in base.cursor.execute(f"SELECT * FROM users"):
            localUsers.insert(len(localUsers), {
                  "username":row[1],
                  "userid":row[2],
                  "discount":row[3],
                  "position_all":row[4],
                  "position_month":row[5],
                  "temp_discount":row[6],
                  "top_discount":row[7]
            })
            count += 1

      print(f"[LocalData]: Loaded {count} users!")
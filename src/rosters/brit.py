from roster import Roster

from vehicles import (acton,
                      amblecote,
                      beerwoods,
                      big_rigg,
                      big_sky,
                      bottlebrook,
                      brass_monkey,
                      brigand,
                      brightling,
                      broadrock,
                      buildwas,
                      buff,
                      capo,
                      catchcan,
                      chainburn,
                      cloud_hill,
                      colbiggan,
                      coldfall,
                      crime_rigg,
                      drumbreck,
                      easywheal,
                      strongbox,
                      fairlop,
                      #foreshore, # deprecated, pending decision on container trucks being in or out
                      fortiscue,
                      foxley,
                      glenmore,
                      goldmire,
                      gravelhead,
                      greenscoe,
                      griff,
                      hawkmoor,
                      highgate,
                      honister,
                      jinglepot,
                      knockdown,
                      ladycross,
                      leyburn,
                      poptop,
                      limebreach,
                      littleduke,
                      mcdowell,
                      meriden,
                      merrivale,
                      nettlebridge,
                      newbold,
                      northbeach,
                      oylbarral,
                      oxleas,
                      pigstick,
                      polangrain,
                      portland,
                      powerstock,
                      quickset,
                      rackwood,
                      rattlebrook,
                      reaver,
                      ribble,
                      road_thief,
                      scrag_end,
                      scrooby_top,
                      shotover,
                      tin_hatch,
                      rakeway,
                      silvertop,
                      singing_river,
                      sparkford,
                      speedwell,
                      stagrun,
                      stakebeck,
                      stancliffe,
                      steeraway,
                      stungun,
                      swineshead,
                      tallyho,
                      thunder,
                      thurlbear,
                      topley,
                      towerhouse,
                      trefell,
                      trotalong,
                      twinhills,
                      waterperry,
                      windergill,
                      winterfold,
                      witch_hill,
                      wookey,
                      yeoman)

roster = Roster(id = 'brit',
                numeric_id = 1,
                truck_speeds = {0: 25, 1905: 40, 1935: 55, 1965: 70, 1985: 80},
                tram_speeds = {0: 25, 1900: 35, 1930: 45, 1960: 55, 1990: 65},
                vehicles = [leyburn,
                            thunder,
                            highgate,
                            topley,
                            glenmore,
                            oxleas,
                            acton,
                            big_sky,
                            tallyho,
                            brass_monkey,
                            goldmire,
                            littleduke,
                            jinglepot,
                            rattlebrook,
                            yeoman,
                            capo,
                            easywheal,
                            quickset,
                            speedwell,
                            chainburn,
                            windergill,
                            towerhouse,
                            big_rigg,
                            honister,
                            wookey,
                            powerstock,
                            greenscoe,
                            meriden,
                            cloud_hill,
                            limebreach,
                            ribble,
                            mcdowell,
                            pigstick,
                            swineshead,
                            stungun,
                            beerwoods,
                            waterperry,
                            silvertop,
                            merrivale,
                            fortiscue,
                            coldfall,
                            #foreshore, # deprecated, pending decision on container trucks being in or out
                            reaver,
                            crime_rigg,
                            brigand,
                            road_thief,
                            # trams
                            ladycross,
                            fairlop,
                            newbold,
                            northbeach,
                            twinhills,
                            tin_hatch,
                            foxley,
                            stagrun,
                            strongbox,
                            singing_river,
                            buildwas,
                            portland,
                            brightling,
                            amblecote,
                            rakeway,
                            colbiggan,
                            stakebeck,
                            rackwood,
                            stancliffe,
                            scrooby_top,
                            hawkmoor,
                            nettlebridge,
                            drumbreck,
                            catchcan,
                            oylbarral,
                            polangrain,
                            thurlbear,
                            scrag_end,
                            trotalong,
                            shotover,
                            poptop,
                            bottlebrook,
                            winterfold,
                            sparkford,
                            # off-highway
                            gravelhead,
                            broadrock,
                            witch_hill,
                            griff,
                            trefell,
                            knockdown,
                            buff,
                            steeraway])

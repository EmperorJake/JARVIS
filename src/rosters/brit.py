from roster import Roster

from vehicles import (acton,
                      amblecote,
                      beerwoods,
                      big_rigg,
                      # big_sky, deprecated
                      bottlebrook,
                      brass_monkey,
                      brigand,
                      brightling,
                      buildwas,
                      buff,
                      capo,
                      catchcan,
                      chainburn,
                      cloud_hill,
                      colbiggan,
                      coldfall,
                      coleman,
                      cowsleigh,
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
                      rakeway,
                      rattlebrook,
                      reaver,
                      ribble,
                      road_thief,
                      runwell,
                      scrag_end,
                      scrooby_top,
                      shotover,
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
                      tin_hatch,
                      topley,
                      towerhouse,
                      trefell,
                      trotalong,
                      twinhills,
                      waterperry,
                      windergill,
                      winterfold,
                      wookey,
                      yeoman)

roster = Roster(id = 'brit',
                numeric_id = 1,
                # keep dates for power and speeds matched
                truck_speeds = {0: 25, 1905: 40, 1935: 55, 1965: 70, 1985: 80},
                tram_speeds = {0: 25, 1900: 35, 1930: 45, 1960: 55, 1990: 65},
                truck_power_bands = {0: 100, 1905: 150, 1935: 250, 1965: 450, 1985: 700},
                tram_power_bands = {0: 100, 1900: 200, 1930: 350, 1960: 550, 1990: 800},
                vehicles = [leyburn,
                            thunder,
                            highgate,
                            topley,
                            glenmore,
                            oxleas,
                            acton,
                            # big_sky, deprecated
                            tallyho,
                            brass_monkey,
                            goldmire,
                            littleduke,
                            jinglepot,
                            rattlebrook,
                            yeoman,
                            capo,
                            runwell,
                            easywheal,
                            quickset,
                            speedwell,
                            chainburn,
                            windergill,
                            towerhouse,
                            big_rigg,
                            coleman,
                            honister,
                            wookey,
                            powerstock,
                            greenscoe,
                            meriden,
                            cloud_hill,
                            limebreach,
                            ribble,
                            mcdowell,
                            cowsleigh,
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
                            griff,
                            trefell,
                            knockdown,
                            buff,
                            steeraway])

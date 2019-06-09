from road_vehicle import MailTruckConsist, DieselVehicleUnit

consist = MailTruckConsist(id='tallyho_mail',
                    base_numeric_id=450,
                    name='Tallyho',
                    power=90,
                    gen=2,
                    intro_date_offset=-1)  # introduce earlier than gen epoch by design

consist.add_unit(type=DieselVehicleUnit,
                 vehicle_length=6)

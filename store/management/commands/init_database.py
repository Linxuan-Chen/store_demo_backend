from django.core.management.base import BaseCommand
from django.db import connection, DatabaseError, transaction


class Command(BaseCommand):
    help = 'init database using sql statements'

    def handle(self, *args, **options):
        sql_statements = [
            '''
                INSERT INTO store_collection (id, title, featured_product_id)
                VALUES  (2, 'Grocery', null),
                        (3, 'Beauty', null),
                        (4, 'Cleaning', null),
                        (5, 'Stationary', null),
                        (6, 'Pets', null),
                        (7, 'Baking', null),
                        (8, 'Spices', null),
                        (9, 'Toys', null),
                        (10, 'Magazines', null);
            ''',
            '''
                INSERT INTO store_product (id, title, description, unit_price, inventory, last_updated, collection_id, slug)
                VALUES  (1, 'Bread Ww Cluster', 'mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus', 4.00, 11, '2020-09-11 00:00:00', 6, '-'),
                        (2, 'Island Oasis - Raspberry', 'maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque', 84.64, 40, '2020-07-07 00:00:00', 3, '-'),
                        (3, 'Shrimp - 21/25, Peel And Deviened', 'nisi volutpat eleifend donec ut dolor morbi vel lectus in quam', 11.52, 29, '2021-04-05 00:00:00', 3, '-'),
                        (4, 'Wood Chips - Regular', 'posuere cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin ut', 73.47, 40, '2020-07-20 00:00:00', 5, '-'),
                        (5, 'Lettuce - Mini Greens, Whole', 'lectus in est risus auctor sed tristique in tempus sit amet sem fusce consequat nulla nisl nunc', 60.21, 56, '2020-08-18 00:00:00', 5, '-'),
                        (6, 'Mustard - Individual Pkg', 'pellentesque volutpat dui maecenas tristique est et tempus semper est quam pharetra magna', 76.62, 18, '2020-10-25 00:00:00', 6, '-'),
                        (7, 'Turkey Tenderloin Frozen', 'sit amet erat nulla tempus vivamus in felis eu sapien cursus vestibulum proin eu mi nulla ac enim', 13.64, 48, '2020-08-08 00:00:00', 4, '-'),
                        (8, 'Silicone Parch. 16.3x24.3', 'faucibus orci luctus et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis', 85.76, 55, '2021-06-03 00:00:00', 6, '-'),
                        (9, 'Tomatoes - Cherry, Yellow', 'sapien cursus vestibulum proin eu mi nulla ac enim in tempor turpis nec euismod scelerisque quam turpis adipiscing', 30.81, 45, '2021-03-03 00:00:00', 5, '-'),
                        (10, 'Sloe Gin - Mcguinness', 'fringilla rhoncus mauris enim leo rhoncus sed vestibulum sit amet cursus id turpis integer aliquet massa', 2.82, 69, '2021-04-18 00:00:00', 5, '-'),
                        (11, 'Wine - Magnotta - Belpaese', 'ut massa volutpat convallis morbi odio odio elementum eu interdum eu tincidunt in leo', 37.72, 71, '2021-01-19 00:00:00', 6, '-'),
                        (12, 'Beer - Alexander Kieths, Pale Ale', 'nisl aenean lectus pellentesque eget nunc donec quis orci eget orci vehicula condimentum curabitur in libero ut massa', 92.74, 55, '2020-12-28 00:00:00', 3, '-'),
                        (13, 'Basil - Thai', 'rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum', 50.07, 41, '2020-07-07 00:00:00', 6, '-'),
                        (14, 'Tofu - Soft', 'at vulputate vitae nisl aenean lectus pellentesque eget nunc donec quis orci eget orci vehicula', 88.70, 24, '2020-08-29 00:00:00', 4, '-'),
                        (15, 'Mayonnaise - Individual Pkg', 'id luctus nec molestie sed justo pellentesque viverra pede ac diam cras pellentesque volutpat dui maecenas tristique est et', 81.81, 35, '2020-07-25 00:00:00', 4, '-'),
                        (16, 'Sauce - Hollandaise', 'blandit lacinia erat vestibulum sed magna at nunc commodo placerat praesent blandit nam nulla integer pede', 9.09, 63, '2020-07-16 00:00:00', 6, '-'),
                        (17, 'Salt - Rock, Course', 'congue etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut', 41.53, 60, '2021-03-05 00:00:00', 3, '-'),
                        (18, 'Beef - Ox Tail, Frozen', 'donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien', 80.97, 85, '2020-07-26 00:00:00', 4, '-'),
                        (19, 'Schnappes - Peach, Walkers', 'phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in', 81.97, 10, '2021-05-14 00:00:00', 5, '-'),
                        (20, 'Cheese - Parmesan Cubes', 'ut nunc vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae mauris viverra', 32.94, 97, '2020-08-12 00:00:00', 3, '-'),
                        (21, 'Sweet Pea Sprouts', 'lectus aliquam sit amet diam in magna bibendum imperdiet nullam', 31.93, 49, '2021-01-14 00:00:00', 5, '-'),
                        (22, 'Straw - Regular', 'nec nisi vulputate nonummy maecenas tincidunt lacus at velit vivamus vel', 76.59, 56, '2020-11-13 00:00:00', 5, '-'),
                        (23, 'Peach - Fresh', 'feugiat et eros vestibulum ac est lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien', 2.95, 63, '2021-01-22 00:00:00', 6, '-'),
                        (24, 'Chinese Foods - Pepper Beef', 'nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris', 86.30, 64, '2020-10-31 00:00:00', 3, '-'),
                        (25, 'Guava', 'erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a', 17.53, 96, '2021-05-05 00:00:00', 4, '-'),
                        (26, 'Tendrils - Baby Pea, Organic', 'lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat', 18.18, 0, '2021-03-24 00:00:00', 3, '-'),
                        (27, 'Sugar - Brown', 'lobortis sapien sapien non mi integer ac neque duis bibendum morbi non quam nec dui', 65.01, 84, '2020-10-24 00:00:00', 5, '-'),
                        (28, 'Oil - Pumpkinseed', 'cursus vestibulum proin eu mi nulla ac enim in tempor turpis nec euismod scelerisque quam turpis', 86.27, 90, '2021-02-11 00:00:00', 5, '-'),
                        (29, 'Beef - Tongue, Cooked', 'sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo', 73.48, 82, '2021-02-07 00:00:00', 6, '-'),
                        (30, 'Goat - Leg', 'vehicula condimentum curabitur in libero ut massa volutpat convallis morbi odio odio elementum eu interdum eu tincidunt in', 83.98, 66, '2021-03-01 00:00:00', 4, '-'),
                        (31, 'Orange Roughy 4/6 Oz', 'id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie', 99.48, 79, '2021-05-26 00:00:00', 5, '-'),
                        (32, 'Lemons', 'et ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit', 29.08, 83, '2021-06-03 00:00:00', 5, '-'),
                        (33, 'Turnip - Mini', 'id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat', 13.93, 8, '2021-03-23 00:00:00', 6, '-'),
                        (34, 'Hinge W Undercut', 'in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices', 20.24, 45, '2020-08-23 00:00:00', 3, '-'),
                        (35, 'Cheese - Mozzarella', 'nam ultrices libero non mattis pulvinar nulla pede ullamcorper augue a suscipit nulla', 34.71, 76, '2020-10-13 00:00:00', 3, '-'),
                        (36, 'Basil - Fresh', 'pede libero quis orci nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras in purus eu', 11.80, 2, '2021-06-07 00:00:00', 4, '-'),
                        (37, 'Pastry - Choclate Baked', 'rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed magna at', 61.87, 12, '2020-11-17 00:00:00', 3, '-'),
                        (38, 'Vol Au Vents', 'non mauris morbi non lectus aliquam sit amet diam in', 81.78, 98, '2021-04-29 00:00:00', 5, '-'),
                        (39, 'Tomatoes - Roma', 'turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum', 29.81, 61, '2020-09-04 00:00:00', 4, '-'),
                        (40, 'Bread - Hamburger Buns', 'vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget', 51.39, 8, '2021-04-07 00:00:00', 5, '-'),
                        (41, 'Cheese - Cambozola', 'vitae quam suspendisse potenti nullam porttitor lacus at turpis donec posuere metus vitae ipsum aliquam non mauris morbi non', 64.20, 54, '2020-12-22 00:00:00', 3, '-'),
                        (42, 'Cup - 4oz Translucent', 'mattis odio donec vitae nisi nam ultrices libero non mattis pulvinar nulla pede ullamcorper augue a', 71.97, 52, '2020-08-29 00:00:00', 5, '-'),
                        (43, 'Macaroons - Two Bite Choc', 'tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus vivamus in felis eu sapien', 14.87, 38, '2021-05-15 00:00:00', 6, '-'),
                        (44, 'Vinegar - Raspberry', 'platea dictumst maecenas ut massa quis augue luctus tincidunt nulla mollis molestie', 52.43, 88, '2021-02-10 00:00:00', 6, '-'),
                        (45, 'Cake - Night And Day Choclate', 'magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non mi integer', 84.60, 93, '2020-09-26 00:00:00', 3, '-'),
                        (46, 'Wine - Domaine Boyar Royal', 'ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo etiam', 39.61, 92, '2020-07-14 00:00:00', 6, '-'),
                        (47, 'Sword Pick Asst', 'nibh in hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer', 75.08, 15, '2021-04-28 00:00:00', 3, '-'),
                        (48, 'Sage - Ground', 'ligula suspendisse ornare consequat lectus in est risus auctor sed tristique in tempus sit amet sem fusce consequat nulla nisl', 16.75, 94, '2021-06-06 00:00:00', 6, '-'),
                        (49, 'Muffin Mix - Chocolate Chip', 'ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis vel', 93.49, 16, '2020-07-07 00:00:00', 3, '-'),
                        (50, 'Tia Maria', 'morbi a ipsum integer a nibh in quis justo maecenas rhoncus aliquam', 69.22, 14, '2020-06-11 00:00:00', 4, '-'),
                        (51, 'Apple - Fuji', 'in lectus pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate luctus cum sociis natoque penatibus', 20.42, 94, '2021-05-05 00:00:00', 3, '-'),
                        (52, 'Veal - Tenderloin, Untrimmed', 'cubilia curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien', 89.46, 44, '2020-06-14 00:00:00', 4, '-'),
                        (53, 'Mushroom - Crimini', 'ut massa quis augue luctus tincidunt nulla mollis molestie lorem quisque ut erat curabitur', 42.13, 58, '2021-01-19 00:00:00', 3, '-'),
                        (54, 'Parsley Italian - Fresh', 'rhoncus mauris enim leo rhoncus sed vestibulum sit amet cursus id turpis', 85.92, 93, '2021-04-24 00:00:00', 3, '-'),
                        (55, 'Tart - Pecan Butter Squares', 'in porttitor pede justo eu massa donec dapibus duis at velit eu est congue elementum in hac habitasse platea dictumst', 91.98, 43, '2020-09-06 00:00:00', 4, '-'),
                        (56, 'Vinegar - Tarragon', 'orci vehicula condimentum curabitur in libero ut massa volutpat convallis morbi odio odio elementum eu interdum', 7.30, 60, '2021-05-09 00:00:00', 5, '-'),
                        (57, 'Beef - Tender Tips', 'nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate luctus cum', 8.83, 5, '2021-01-01 00:00:00', 3, '-'),
                        (58, 'Chicken - Whole Roasting', 'id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci', 47.43, 11, '2021-04-07 00:00:00', 3, '-'),
                        (59, 'Water - Tonic', 'sit amet eleifend pede libero quis orci nullam molestie nibh', 36.84, 13, '2020-08-14 00:00:00', 6, '-'),
                        (60, 'Shrimp - Tiger 21/25', 'nibh in hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer', 64.38, 100, '2020-07-21 00:00:00', 4, '-'),
                        (61, 'Hagen Daza - Dk Choocolate', 'sit amet sapien dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere', 37.63, 43, '2020-09-25 00:00:00', 6, '-'),
                        (62, 'Grenadillo', 'lorem ipsum dolor sit amet consectetuer adipiscing elit proin risus praesent lectus vestibulum quam sapien varius', 14.57, 34, '2020-10-14 00:00:00', 6, '-'),
                        (63, 'Coffee - 10oz Cup 92961', 'quam fringilla rhoncus mauris enim leo rhoncus sed vestibulum sit amet', 26.36, 34, '2020-09-22 00:00:00', 5, '-'),
                        (64, 'Seabream Whole Farmed', 'interdum eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus vivamus in felis', 59.91, 32, '2021-02-13 00:00:00', 5, '-'),
                        (65, 'Coconut Milk - Unsweetened', 'felis eu sapien cursus vestibulum proin eu mi nulla ac enim in tempor turpis nec euismod scelerisque', 79.79, 12, '2021-03-10 00:00:00', 4, '-'),
                        (66, 'Soap - Mr.clean Floor Soap', 'consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum', 38.03, 31, '2020-06-13 00:00:00', 5, '-'),
                        (67, 'Cheese - Cambozola', 'tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed magna at nunc', 19.49, 33, '2021-01-13 00:00:00', 5, '-'),
                        (68, 'Soup Campbells Mexicali Tortilla', 'pulvinar sed nisl nunc rhoncus dui vel sem sed sagittis nam congue risus semper porta volutpat', 93.16, 7, '2021-04-14 00:00:00', 5, '-'),
                        (69, 'Apron', 'amet eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque at nulla suspendisse', 4.66, 6, '2021-02-10 00:00:00', 4, '-'),
                        (70, 'Wine - Penfolds Koonuga Hill', 'aenean auctor gravida sem praesent id massa id nisl venenatis lacinia aenean sit amet justo morbi ut', 1.27, 15, '2020-12-10 00:00:00', 3, '-'),
                        (71, 'Milk - Chocolate 250 Ml', 'gravida sem praesent id massa id nisl venenatis lacinia aenean sit amet justo morbi ut odio cras', 1.88, 25, '2020-08-19 00:00:00', 5, '-'),
                        (72, 'Beer - Paulaner Hefeweisse', 'lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci', 36.96, 43, '2020-10-10 00:00:00', 4, '-'),
                        (73, 'Chocolate - Feathers', 'ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae mauris', 65.35, 50, '2020-11-02 00:00:00', 4, '-'),
                        (74, 'Club Soda - Schweppes, 355 Ml', 'duis bibendum felis sed interdum venenatis turpis enim blandit mi in porttitor pede justo eu massa donec dapibus duis at', 90.39, 72, '2021-04-13 00:00:00', 3, '-'),
                        (75, 'Corn Kernels - Frozen', 'odio cras mi pede malesuada in imperdiet et commodo vulputate justo in blandit ultrices enim lorem ipsum', 98.61, 53, '2020-10-12 00:00:00', 4, '-'),
                        (76, 'Cheese Cloth No 60', 'posuere metus vitae ipsum aliquam non mauris morbi non lectus aliquam sit amet', 66.25, 72, '2020-12-08 00:00:00', 3, '-'),
                        (77, 'Chips - Assorted', 'nascetur ridiculus mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus', 86.36, 93, '2020-07-06 00:00:00', 3, '-'),
                        (78, 'Bagelers', 'eget eleifend luctus ultricies eu nibh quisque id justo sit amet sapien dignissim', 82.37, 39, '2020-08-29 00:00:00', 4, '-'),
                        (79, 'Corn - Cream, Canned', 'in consequat ut nulla sed accumsan felis ut at dolor quis odio consequat varius integer ac leo pellentesque', 85.46, 24, '2021-05-13 00:00:00', 3, '-'),
                        (80, 'Bread - Raisin', 'donec diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum primis', 8.70, 70, '2020-07-09 00:00:00', 4, '-'),
                        (81, 'Soup - Campbells', 'turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci', 8.13, 29, '2020-12-15 00:00:00', 5, '-'),
                        (82, 'Ecolab - Hobart Washarm End Cap', 'placerat praesent blandit nam nulla integer pede justo lacinia eget tincidunt', 83.36, 67, '2020-10-25 00:00:00', 5, '-'),
                        (83, 'Asparagus - White, Canned', 'in porttitor pede justo eu massa donec dapibus duis at velit eu est congue elementum in hac habitasse platea dictumst', 71.01, 17, '2020-07-27 00:00:00', 3, '-'),
                        (84, 'Muffin Mix - Lemon Cranberry', 'ipsum praesent blandit lacinia erat vestibulum sed magna at nunc commodo placerat praesent blandit nam nulla integer pede justo', 47.63, 11, '2020-12-23 00:00:00', 6, '-'),
                        (85, 'Shrimp - 16/20, Peeled Deviened', 'parturient montes nascetur ridiculus mus etiam vel augue vestibulum rutrum rutrum neque aenean auctor', 1.08, 58, '2021-06-07 00:00:00', 5, '-'),
                        (86, 'Soda Water - Club Soda, 355 Ml', 'faucibus accumsan odio curabitur convallis duis consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus', 90.06, 88, '2021-05-04 00:00:00', 3, '-'),
                        (87, 'Napkin White - Starched', 'quam nec dui luctus rutrum nulla tellus in sagittis dui', 30.95, 52, '2020-10-10 00:00:00', 5, '-'),
                        (88, 'Beer - Steamwhistle', 'nulla justo aliquam quis turpis eget elit sodales scelerisque mauris sit amet', 11.89, 59, '2020-06-20 00:00:00', 3, '-'),
                        (89, 'Pail For Lid 1537', 'in ante vestibulum ante ipsum primis in faucibus orci luctus et ultrices', 35.85, 92, '2020-10-11 00:00:00', 6, '-'),
                        (90, 'Chinese Foods - Chicken Wing', 'purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus', 28.87, 48, '2020-12-28 00:00:00', 3, '-'),
                        (91, 'Spice - Montreal Steak Spice', 'donec dapibus duis at velit eu est congue elementum in', 35.71, 32, '2021-05-15 00:00:00', 5, '-'),
                        (92, 'Juice - Grapefruit, 341 Ml', 'vestibulum proin eu mi nulla ac enim in tempor turpis nec', 33.37, 26, '2020-07-16 00:00:00', 5, '-'),
                        (93, 'Wine - Wyndham Estate Bin 777', 'pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est risus auctor sed tristique in tempus', 3.34, 87, '2020-12-29 00:00:00', 5, '-'),
                        (94, 'Water - Mineral, Natural', 'pretium quis lectus suspendisse potenti in eleifend quam a odio in hac', 61.59, 71, '2020-07-16 00:00:00', 5, '-'),
                        (95, 'Chicken - Leg, Boneless', 'eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero nam dui proin', 84.83, 15, '2020-06-21 00:00:00', 3, '-'),
                        (96, 'Sunflower Seed Raw', 'volutpat dui maecenas tristique est et tempus semper est quam pharetra magna ac consequat', 28.16, 2, '2020-10-19 00:00:00', 3, '-'),
                        (97, 'Energy Drink Bawls', 'risus praesent lectus vestibulum quam sapien varius ut blandit non', 87.65, 31, '2021-02-23 00:00:00', 6, '-'),
                        (98, 'Tarragon - Primerba, Paste', 'non quam nec dui luctus rutrum nulla tellus in sagittis', 20.87, 38, '2020-08-11 00:00:00', 3, '-'),
                        (99, 'Table Cloth 62x120 Colour', 'et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis', 27.91, 96, '2021-03-20 00:00:00', 3, '-'),
                        (100, 'Lamb - Loin Chops', 'praesent id massa id nisl venenatis lacinia aenean sit amet justo', 87.47, 40, '2021-02-20 00:00:00', 3, '-'),
                        (101, 'Sherry - Dry', 'morbi ut odio cras mi pede malesuada in imperdiet et commodo vulputate justo in blandit', 70.52, 32, '2020-06-27 00:00:00', 6, '-'),
                        (102, 'Chickensplit Half', 'congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue', 93.81, 66, '2021-03-02 00:00:00', 4, '-'),
                        (103, 'Tea - Orange Pekoe', 'vel enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus', 12.71, 77, '2020-07-12 00:00:00', 3, '-'),
                        (104, 'Sauce - Caesar Dressing', 'orci luctus et ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis', 98.89, 62, '2020-09-03 00:00:00', 3, '-'),
                        (105, 'Rice - Brown', 'lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec molestie sed justo pellentesque viverra', 83.88, 24, '2020-06-20 00:00:00', 6, '-'),
                        (106, 'Soup - Knorr, Ministrone', 'rutrum rutrum neque aenean auctor gravida sem praesent id massa id nisl venenatis lacinia', 4.88, 22, '2020-07-30 00:00:00', 5, '-'),
                        (107, 'Wine - Cotes Du Rhone Parallele', 'risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam', 13.89, 10, '2021-04-13 00:00:00', 3, '-'),
                        (108, 'Chips Potato All Dressed - 43g', 'faucibus accumsan odio curabitur convallis duis consequat dui nec nisi', 35.65, 13, '2020-10-23 00:00:00', 3, '-'),
                        (109, 'Sugar - Crumb', 'aliquet at feugiat non pretium quis lectus suspendisse potenti in eleifend quam a odio in hac habitasse platea', 5.07, 95, '2021-01-08 00:00:00', 3, '-'),
                        (110, 'Ice Cream - Strawberry', 'posuere felis sed lacus morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc rhoncus dui vel', 22.63, 7, '2021-04-06 00:00:00', 4, '-'),
                        (111, 'Paper Cocktail Umberlla 80 - 180', 'sit amet justo morbi ut odio cras mi pede malesuada in imperdiet et commodo vulputate', 94.11, 94, '2021-04-14 00:00:00', 3, '-'),
                        (112, 'Salmon - Canned', 'est quam pharetra magna ac consequat metus sapien ut nunc vestibulum ante ipsum primis in faucibus orci luctus et', 80.67, 59, '2021-02-26 00:00:00', 6, '-'),
                        (113, 'Seedlings - Buckwheat, Organic', 'vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus', 44.29, 80, '2020-08-14 00:00:00', 5, '-'),
                        (114, 'Cheese - Brie, Triple Creme', 'sed magna at nunc commodo placerat praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget tempus', 46.60, 66, '2020-08-06 00:00:00', 3, '-'),
                        (115, 'Phyllo Dough', 'risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam sit amet turpis elementum ligula', 35.53, 45, '2021-02-03 00:00:00', 3, '-'),
                        (116, 'Pastry - Banana Muffin - Mini', 'vivamus tortor duis mattis egestas metus aenean fermentum donec ut mauris eget massa', 85.57, 59, '2020-12-29 00:00:00', 4, '-'),
                        (117, 'Jameson - Irish Whiskey', 'non mattis pulvinar nulla pede ullamcorper augue a suscipit nulla elit ac nulla sed vel', 65.52, 97, '2020-11-25 00:00:00', 3, '-'),
                        (118, 'Praline Paste', 'in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc donec', 57.27, 3, '2021-04-02 00:00:00', 3, '-'),
                        (119, 'Flour - Fast / Rapid', 'suspendisse potenti nullam porttitor lacus at turpis donec posuere metus vitae', 77.83, 79, '2020-11-03 00:00:00', 5, '-'),
                        (120, 'Sausage - Meat', 'enim in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem', 49.77, 44, '2020-06-22 00:00:00', 6, '-'),
                        (121, 'Wine - Vovray Sec Domaine Huet', 'tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut', 2.20, 84, '2021-01-11 00:00:00', 4, '-'),
                        (122, 'Ecolab - Hand Soap Form Antibac', 'amet eros suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum donec ut', 44.58, 96, '2020-09-17 00:00:00', 4, '-'),
                        (123, 'Melon - Honey Dew', 'quam pede lobortis ligula sit amet eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque at nulla suspendisse', 57.94, 55, '2021-04-24 00:00:00', 4, '-'),
                        (124, 'Dill - Primerba, Paste', 'ac neque duis bibendum morbi non quam nec dui luctus rutrum nulla tellus in sagittis dui vel nisl', 97.81, 72, '2020-11-11 00:00:00', 6, '-'),
                        (125, 'Pork - Ham, Virginia', 'sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean lectus', 97.58, 74, '2021-03-06 00:00:00', 3, '-'),
                        (126, 'Pasta - Cannelloni, Sheets, Fresh', 'mauris morbi non lectus aliquam sit amet diam in magna bibendum imperdiet nullam orci pede venenatis', 86.27, 5, '2021-01-20 00:00:00', 3, '-'),
                        (127, 'Apple - Macintosh', 'volutpat in congue etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus', 19.96, 45, '2021-01-07 00:00:00', 6, '-'),
                        (128, 'Vodka - Moskovskaya', 'ac tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis', 43.45, 74, '2021-04-19 00:00:00', 6, '-'),
                        (129, 'Curry Powder', 'vitae consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum', 32.31, 42, '2021-01-30 00:00:00', 4, '-'),
                        (130, 'Sauce - Vodka Blush', 'a suscipit nulla elit ac nulla sed vel enim sit amet nunc viverra dapibus', 53.31, 27, '2020-07-20 00:00:00', 6, '-'),
                        (131, 'Venison - Ground', 'vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non pretium quis lectus suspendisse potenti in', 15.76, 26, '2021-05-13 00:00:00', 4, '-'),
                        (132, 'Doilies - 8, Paper', 'maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros', 46.59, 79, '2020-09-09 00:00:00', 6, '-'),
                        (133, 'Vaccum Bag - 14x20', 'vestibulum proin eu mi nulla ac enim in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae', 57.26, 15, '2021-01-08 00:00:00', 6, '-'),
                        (134, 'Gherkin', 'nunc vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere', 8.68, 94, '2020-08-20 00:00:00', 3, '-'),
                        (135, 'Water - Mineral, Natural', 'morbi odio odio elementum eu interdum eu tincidunt in leo', 58.27, 17, '2021-05-13 00:00:00', 3, '-'),
                        (136, 'Ecolab - Solid Fusion', 'magna at nunc commodo placerat praesent blandit nam nulla integer', 94.84, 71, '2021-03-22 00:00:00', 5, '-'),
                        (137, 'Bar - Sweet And Salty Chocolate', 'erat volutpat in congue etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus', 50.15, 46, '2020-07-03 00:00:00', 3, '-'),
                        (138, 'Spice - Peppercorn Melange', 'dapibus augue vel accumsan tellus nisi eu orci mauris lacinia', 86.52, 58, '2020-12-29 00:00:00', 4, '-'),
                        (139, 'Chicken Breast Wing On', 'fusce posuere felis sed lacus morbi sem mauris laoreet ut rhoncus aliquet', 42.81, 31, '2020-06-21 00:00:00', 5, '-'),
                        (140, 'Sauce - Roasted Red Pepper', 'pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo etiam pretium', 39.14, 35, '2021-01-13 00:00:00', 5, '-'),
                        (141, 'Mackerel Whole Fresh', 'at nibh in hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer tincidunt ante', 24.36, 98, '2021-02-08 00:00:00', 3, '-'),
                        (142, 'Glass Clear 8 Oz', 'in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu', 4.34, 97, '2020-08-11 00:00:00', 6, '-'),
                        (143, 'Soup - Campbells, Spinach Crm', 'diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat', 15.47, 18, '2021-01-03 00:00:00', 3, '-'),
                        (144, 'Pork Salted Bellies', 'morbi a ipsum integer a nibh in quis justo maecenas rhoncus', 61.50, 50, '2021-04-14 00:00:00', 6, '-'),
                        (145, 'Juice - Pineapple, 48 Oz', 'accumsan odio curabitur convallis duis consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus in', 73.24, 31, '2020-09-08 00:00:00', 4, '-'),
                        (146, 'Cheese - Comtomme', 'fermentum justo nec condimentum neque sapien placerat ante nulla justo', 20.58, 65, '2020-11-27 00:00:00', 6, '-'),
                        (147, 'Cookie Dough - Peanut Butter', 'consequat nulla nisl nunc nisl duis bibendum felis sed interdum', 49.25, 71, '2020-07-14 00:00:00', 5, '-'),
                        (148, 'Paste - Black Olive', 'sit amet justo morbi ut odio cras mi pede malesuada', 55.51, 49, '2020-10-17 00:00:00', 3, '-'),
                        (149, 'Lettuce - Treviso', 'malesuada in imperdiet et commodo vulputate justo in blandit ultrices enim lorem ipsum dolor', 56.29, 92, '2020-08-21 00:00:00', 3, '-'),
                        (150, 'Tea - Lemon Green Tea', 'commodo placerat praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem id', 70.09, 10, '2020-09-16 00:00:00', 3, '-'),
                        (151, 'Lettuce - Curly Endive', 'maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus vivamus in felis eu sapien', 60.41, 27, '2021-04-19 00:00:00', 5, '-'),
                        (152, 'Vinegar - Balsamic', 'eget elit sodales scelerisque mauris sit amet eros suspendisse accumsan tortor quis', 8.40, 15, '2020-07-17 00:00:00', 6, '-'),
                        (153, 'Cheese - Brie Roitelet', 'in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus', 80.45, 69, '2021-06-07 00:00:00', 4, '-'),
                        (154, 'Tomatoes - Diced, Canned', 'justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat id mauris vulputate elementum', 47.43, 41, '2020-07-31 00:00:00', 4, '-'),
                        (155, 'Muffin Mix - Morning Glory', 'tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis', 62.77, 56, '2020-09-05 00:00:00', 3, '-'),
                        (156, 'Yogurt - Cherry, 175 Gr', 'mi integer ac neque duis bibendum morbi non quam nec dui luctus rutrum nulla tellus in', 27.78, 86, '2020-08-18 00:00:00', 6, '-'),
                        (157, 'Food Colouring - Green', 'dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus', 69.86, 29, '2020-09-25 00:00:00', 4, '-'),
                        (158, 'Eel Fresh', 'primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus', 40.25, 28, '2021-02-06 00:00:00', 5, '-'),
                        (159, 'Lemonade - Strawberry, 591 Ml', 'justo in hac habitasse platea dictumst etiam faucibus cursus urna', 7.04, 7, '2020-10-02 00:00:00', 6, '-'),
                        (160, 'Cod - Salted, Boneless', 'magnis dis parturient montes nascetur ridiculus mus vivamus vestibulum sagittis sapien', 37.31, 91, '2021-01-25 00:00:00', 4, '-'),
                        (161, 'Jam - Strawberry, 20 Ml Jar', 'elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy', 25.74, 10, '2020-08-10 00:00:00', 3, '-'),
                        (162, 'Veal - Inside Round / Top, Lean', 'ultricies eu nibh quisque id justo sit amet sapien dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et', 72.51, 85, '2021-05-19 00:00:00', 6, '-'),
                        (163, 'Lemonade - Pineapple Passion', 'nec molestie sed justo pellentesque viverra pede ac diam cras pellentesque volutpat dui maecenas tristique', 14.67, 8, '2021-04-23 00:00:00', 3, '-'),
                        (164, 'Peach - Fresh', 'non sodales sed tincidunt eu felis fusce posuere felis sed lacus morbi', 74.71, 51, '2021-06-08 00:00:00', 5, '-'),
                        (165, 'Garlic', 'nascetur ridiculus mus etiam vel augue vestibulum rutrum rutrum neque aenean auctor gravida sem praesent id massa id', 85.06, 64, '2021-01-18 00:00:00', 4, '-'),
                        (166, 'Artichoke - Fresh', 'pede malesuada in imperdiet et commodo vulputate justo in blandit ultrices enim lorem ipsum dolor sit amet consectetuer adipiscing', 70.35, 100, '2020-09-27 00:00:00', 6, '-'),
                        (167, 'Sauce - Thousand Island', 'orci luctus et ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis', 35.45, 64, '2021-03-02 00:00:00', 3, '-'),
                        (168, 'Sparkling Wine - Rose, Freixenet', 'augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed', 73.38, 45, '2020-11-28 00:00:00', 4, '-'),
                        (169, 'Cheese - Cheddar, Medium', 'tempus sit amet sem fusce consequat nulla nisl nunc nisl duis', 80.33, 95, '2020-11-09 00:00:00', 3, '-'),
                        (170, 'Yeast Dry - Fleischman', 'adipiscing elit proin interdum mauris non ligula pellentesque ultrices phasellus id sapien in sapien', 46.37, 39, '2020-06-17 00:00:00', 4, '-'),
                        (171, 'Chips - Potato Jalapeno', 'augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam sit amet turpis', 30.96, 9, '2021-03-07 00:00:00', 4, '-'),
                        (172, 'Shallots', 'sit amet consectetuer adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante', 84.84, 87, '2021-02-25 00:00:00', 4, '-'),
                        (173, 'Coke - Diet, 355 Ml', 'eget elit sodales scelerisque mauris sit amet eros suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis', 89.46, 52, '2020-07-20 00:00:00', 3, '-'),
                        (174, 'Pernod', 'condimentum id luctus nec molestie sed justo pellentesque viverra pede ac diam cras pellentesque volutpat dui maecenas tristique est', 68.59, 78, '2021-05-24 00:00:00', 5, '-'),
                        (175, 'Pate - Cognac', 'eu est congue elementum in hac habitasse platea dictumst morbi', 87.37, 3, '2021-05-06 00:00:00', 6, '-'),
                        (176, 'Wine - Penfolds Koonuga Hill', 'vestibulum sit amet cursus id turpis integer aliquet massa id', 43.99, 34, '2020-08-03 00:00:00', 5, '-'),
                        (177, 'Shrimp - Tiger 21/25', 'massa quis augue luctus tincidunt nulla mollis molestie lorem quisque ut erat', 59.91, 4, '2020-07-23 00:00:00', 3, '-'),
                        (178, 'Watercress', 'blandit non interdum in ante vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia', 25.40, 94, '2021-04-14 00:00:00', 4, '-'),
                        (179, 'Flour - Chickpea', 'nonummy maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum', 11.58, 20, '2021-05-25 00:00:00', 6, '-'),
                        (180, 'Tea Leaves - Oolong', 'varius ut blandit non interdum in ante vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia', 9.86, 92, '2021-03-14 00:00:00', 4, '-'),
                        (181, 'Wine - Hardys Bankside Shiraz', 'vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc', 98.46, 69, '2020-12-29 00:00:00', 3, '-'),
                        (182, 'Magnotta - Bel Paese White', 'mattis pulvinar nulla pede ullamcorper augue a suscipit nulla elit', 87.08, 65, '2021-04-24 00:00:00', 5, '-'),
                        (183, 'Beef - Montreal Smoked Brisket', 'vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia', 65.66, 68, '2021-02-25 00:00:00', 5, '-'),
                        (184, 'Doilies - 7, Paper', 'nunc purus phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in', 6.42, 9, '2021-05-09 00:00:00', 4, '-'),
                        (185, 'Venison - Striploin', 'vulputate luctus cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus vivamus vestibulum sagittis sapien cum sociis', 85.15, 88, '2021-02-20 00:00:00', 6, '-'),
                        (186, 'Turnip - Mini', 'ultrices aliquet maecenas leo odio condimentum id luctus nec molestie sed justo pellentesque', 80.88, 67, '2021-02-06 00:00:00', 6, '-'),
                        (187, 'Peach - Halves', 'non interdum in ante vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae duis faucibus', 12.87, 76, '2021-01-01 00:00:00', 3, '-'),
                        (188, 'Glaze - Clear', 'quam a odio in hac habitasse platea dictumst maecenas ut massa', 19.86, 1, '2020-11-12 00:00:00', 3, '-'),
                        (189, 'Wine - Red, Concha Y Toro', 'tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus', 65.45, 24, '2020-11-01 00:00:00', 5, '-'),
                        (190, 'Wine - Ej Gallo Sonoma', 'parturient montes nascetur ridiculus mus etiam vel augue vestibulum rutrum rutrum neque aenean auctor', 91.58, 6, '2021-02-17 00:00:00', 4, '-'),
                        (191, 'Pickles - Gherkins', 'lectus pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis', 68.10, 18, '2020-12-12 00:00:00', 3, '-'),
                        (192, 'Butter Sweet', 'fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu', 39.80, 72, '2020-10-04 00:00:00', 6, '-'),
                        (193, 'Onions - Red Pearl', 'magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non mi integer', 35.52, 51, '2021-05-31 00:00:00', 3, '-'),
                        (194, 'Seedlings - Mix, Organic', 'aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci mauris', 6.23, 51, '2020-11-29 00:00:00', 5, '-'),
                        (195, 'Bread - Calabrese Baguette', 'enim blandit mi in porttitor pede justo eu massa donec dapibus duis at velit eu est congue', 80.51, 43, '2020-07-18 00:00:00', 3, '-'),
                        (196, 'Lamb - Loin Chops', 'libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan', 94.45, 2, '2020-08-07 00:00:00', 5, '-'),
                        (197, 'Peas Snow', 'egestas metus aenean fermentum donec ut mauris eget massa tempor convallis nulla neque libero convallis eget eleifend', 18.05, 93, '2021-06-07 00:00:00', 5, '-'),
                        (198, 'Blueberries', 'a pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante', 74.23, 11, '2021-06-06 00:00:00', 5, '-'),
                        (199, 'Cookie - Dough Variety', 'parturient montes nascetur ridiculus mus etiam vel augue vestibulum rutrum rutrum neque aenean auctor gravida sem praesent id', 37.39, 79, '2021-04-17 00:00:00', 4, '-'),
                        (200, 'Extract - Almond', 'nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien', 9.97, 86, '2021-02-14 00:00:00', 5, '-'),
                        (201, 'Pastry - Banana Muffin - Mini', 'convallis eget eleifend luctus ultricies eu nibh quisque id justo sit amet sapien dignissim vestibulum vestibulum ante', 34.27, 98, '2021-03-05 00:00:00', 4, '-'),
                        (202, 'Food Colouring - Orange', 'quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec', 74.11, 20, '2021-01-31 00:00:00', 5, '-'),
                        (203, 'Split Peas - Green, Dry', 'lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec', 2.51, 77, '2020-08-02 00:00:00', 4, '-'),
                        (204, 'Lid Coffee Cup 8oz Blk', 'mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt', 26.97, 71, '2020-08-27 00:00:00', 3, '-'),
                        (205, 'Truffle Cups Green', 'proin at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum', 88.95, 38, '2021-01-20 00:00:00', 3, '-'),
                        (206, 'Cheese - Sheep Milk', 'risus semper porta volutpat quam pede lobortis ligula sit amet eleifend pede libero quis orci nullam molestie nibh in', 64.43, 87, '2020-11-21 00:00:00', 3, '-'),
                        (207, 'Oil - Shortening - All - Purpose', 'ultrices posuere cubilia curae mauris viverra diam vitae quam suspendisse potenti nullam porttitor lacus at turpis donec posuere', 68.52, 78, '2021-06-09 00:00:00', 6, '-'),
                        (208, 'Pepper - Chillies, Crushed', 'ultrices aliquet maecenas leo odio condimentum id luctus nec molestie', 17.08, 77, '2020-11-08 00:00:00', 5, '-'),
                        (209, 'Chicken - Whole Roasting', 'duis bibendum felis sed interdum venenatis turpis enim blandit mi in porttitor pede', 95.44, 9, '2021-05-06 00:00:00', 5, '-'),
                        (210, 'Wiberg Cure', 'vel est donec odio justo sollicitudin ut suscipit a feugiat et eros vestibulum ac est lacinia nisi venenatis', 52.18, 6, '2021-04-09 00:00:00', 6, '-'),
                        (211, 'Cleaner - Lime Away', 'ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis consequat dui', 78.25, 95, '2020-09-06 00:00:00', 6, '-'),
                        (212, 'Puree - Kiwi', 'ac tellus semper interdum mauris ullamcorper purus sit amet nulla', 49.93, 80, '2020-09-11 00:00:00', 4, '-'),
                        (213, 'Pineapple - Canned, Rings', 'ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis consequat dui nec nisi', 19.07, 23, '2020-07-19 00:00:00', 3, '-'),
                        (214, 'Turkey - Oven Roast Breast', 'adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in', 85.71, 10, '2021-03-31 00:00:00', 3, '-'),
                        (215, 'Hand Towel', 'suspendisse ornare consequat lectus in est risus auctor sed tristique in tempus sit amet sem fusce consequat nulla nisl', 36.16, 54, '2020-09-25 00:00:00', 4, '-'),
                        (216, 'Pork - Sausage, Medium', 'vitae quam suspendisse potenti nullam porttitor lacus at turpis donec', 68.06, 25, '2020-10-31 00:00:00', 3, '-'),
                        (217, 'Cheese Cloth No 100', 'id justo sit amet sapien dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia', 11.95, 52, '2020-12-31 00:00:00', 3, '-'),
                        (218, 'Sobe - Tropical Energy', 'purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient', 24.26, 34, '2021-04-07 00:00:00', 6, '-'),
                        (219, 'Beef - Rib Roast, Capless', 'accumsan felis ut at dolor quis odio consequat varius integer ac leo pellentesque ultrices mattis odio donec', 85.39, 41, '2020-10-28 00:00:00', 5, '-'),
                        (220, 'Beans - Turtle, Black, Dry', 'turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum donec', 40.72, 30, '2020-09-23 00:00:00', 6, '-'),
                        (221, 'Cookie - Oatmeal', 'vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel est donec', 55.05, 33, '2021-03-08 00:00:00', 4, '-'),
                        (222, 'Lettuce - Escarole', 'donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non mi integer ac', 94.97, 46, '2020-11-13 00:00:00', 5, '-'),
                        (223, 'Bread - Bistro White', 'scelerisque mauris sit amet eros suspendisse accumsan tortor quis turpis sed ante vivamus tortor', 36.65, 30, '2021-04-14 00:00:00', 3, '-'),
                        (224, 'English Muffin', 'sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque ultrices', 99.65, 46, '2021-05-24 00:00:00', 6, '-'),
                        (225, 'Table Cloth 54x54 White', 'ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue', 37.58, 54, '2021-03-19 00:00:00', 3, '-'),
                        (226, 'Melon - Watermelon, Seedless', 'sodales sed tincidunt eu felis fusce posuere felis sed lacus morbi sem mauris laoreet ut rhoncus aliquet pulvinar', 57.44, 26, '2021-05-15 00:00:00', 3, '-'),
                        (227, 'Dill Weed - Dry', 'nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis enim blandit', 99.51, 40, '2020-10-26 00:00:00', 3, '-'),
                        (228, 'Pepper Squash', 'pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum', 11.07, 45, '2021-02-14 00:00:00', 5, '-'),
                        (229, 'Flavouring - Orange', 'elit sodales scelerisque mauris sit amet eros suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis', 6.83, 95, '2021-04-06 00:00:00', 5, '-'),
                        (230, 'Spice - Peppercorn Melange', 'felis ut at dolor quis odio consequat varius integer ac leo pellentesque ultrices', 56.29, 49, '2021-05-13 00:00:00', 5, '-'),
                        (231, 'Sprouts - Onion', 'augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat', 5.68, 67, '2021-01-14 00:00:00', 4, '-'),
                        (232, 'Wine - Magnotta - Cab Franc', 'lacinia aenean sit amet justo morbi ut odio cras mi pede malesuada in imperdiet et commodo vulputate justo in blandit', 52.31, 50, '2020-11-21 00:00:00', 4, '-'),
                        (233, 'Cup - 6oz, Foam', 'imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in', 92.28, 97, '2021-04-02 00:00:00', 6, '-'),
                        (234, 'Cake - Dulce De Leche', 'dui vel sem sed sagittis nam congue risus semper porta volutpat quam pede lobortis ligula sit amet', 6.62, 54, '2021-02-01 00:00:00', 3, '-'),
                        (235, 'Greens Mustard', 'dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel', 67.25, 74, '2020-11-28 00:00:00', 3, '-'),
                        (236, 'Kiwano', 'volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in', 27.60, 13, '2020-10-22 00:00:00', 6, '-'),
                        (237, 'Carbonated Water - Wildberry', 'vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla', 54.57, 22, '2020-12-24 00:00:00', 6, '-'),
                        (238, 'Cheese - St. Paulin', 'convallis nunc proin at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate ut', 23.35, 98, '2020-08-11 00:00:00', 3, '-'),
                        (239, 'Wine - Jaboulet Cotes Du Rhone', 'eget nunc donec quis orci eget orci vehicula condimentum curabitur in libero ut massa volutpat', 14.43, 48, '2020-07-13 00:00:00', 5, '-'),
                        (240, 'Pie Box - Cello Window 2.5', 'ullamcorper augue a suscipit nulla elit ac nulla sed vel enim sit', 46.42, 94, '2021-03-30 00:00:00', 4, '-'),
                        (241, 'Brandy - Bar', 'pellentesque ultrices mattis odio donec vitae nisi nam ultrices libero non mattis pulvinar nulla pede ullamcorper augue', 72.33, 96, '2020-09-08 00:00:00', 4, '-'),
                        (242, 'Veal - Slab Bacon', 'ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae donec pharetra magna', 74.61, 69, '2020-11-07 00:00:00', 3, '-'),
                        (243, 'Duck - Whole', 'orci luctus et ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin', 25.38, 73, '2021-05-16 00:00:00', 4, '-'),
                        (244, 'Bagelers', 'id pretium iaculis diam erat fermentum justo nec condimentum neque sapien', 57.79, 92, '2020-08-28 00:00:00', 4, '-'),
                        (245, 'Pepper - Pablano', 'porttitor lacus at turpis donec posuere metus vitae ipsum aliquam', 62.55, 71, '2021-04-19 00:00:00', 6, '-'),
                        (246, 'Mustard - Seed', 'ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim leo rhoncus sed vestibulum sit', 88.31, 65, '2021-02-08 00:00:00', 4, '-'),
                        (247, 'Strawberries', 'libero nullam sit amet turpis elementum ligula vehicula consequat morbi a ipsum', 43.48, 97, '2020-11-12 00:00:00', 3, '-'),
                        (248, 'Cup - Translucent 7 Oz Clear', 'dictumst morbi vestibulum velit id pretium iaculis diam erat fermentum justo nec condimentum neque sapien placerat ante nulla', 54.28, 78, '2021-02-11 00:00:00', 6, '-'),
                        (249, 'Jameson Irish Whiskey', 'bibendum imperdiet nullam orci pede venenatis non sodales sed tincidunt eu felis', 52.91, 54, '2021-02-17 00:00:00', 4, '-'),
                        (250, 'Beef - Eye Of Round', 'magna at nunc commodo placerat praesent blandit nam nulla integer pede justo', 48.84, 7, '2020-10-22 00:00:00', 3, '-'),
                        (251, 'The Pop Shoppe - Grape', 'mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate', 18.35, 5, '2021-04-01 00:00:00', 6, '-'),
                        (252, 'Cheese - Cheddar, Medium', 'enim in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis nibh ligula nec sem duis aliquam convallis', 92.34, 85, '2020-06-10 00:00:00', 3, '-'),
                        (253, 'Tomatoes Tear Drop Yellow', 'pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis', 10.60, 0, '2021-02-08 00:00:00', 3, '-'),
                        (254, 'Extract Vanilla Pure', 'mauris lacinia sapien quis libero nullam sit amet turpis elementum ligula vehicula consequat morbi a ipsum integer a nibh', 10.05, 87, '2021-01-22 00:00:00', 6, '-'),
                        (255, 'Ham - Smoked, Bone - In', 'vel est donec odio justo sollicitudin ut suscipit a feugiat et eros vestibulum ac est lacinia', 83.75, 93, '2020-12-29 00:00:00', 3, '-'),
                        (256, 'Burger Veggie', 'vel enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at', 53.73, 44, '2020-10-09 00:00:00', 3, '-'),
                        (257, 'Appetizer - Sausage Rolls', 'at velit eu est congue elementum in hac habitasse platea dictumst morbi vestibulum velit id', 96.43, 84, '2021-01-14 00:00:00', 5, '-'),
                        (258, 'Wine - Magnotta - Pinot Gris Sr', 'nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris', 26.42, 2, '2021-02-17 00:00:00', 4, '-'),
                        (259, 'Melon - Watermelon Yellow', 'sit amet justo morbi ut odio cras mi pede malesuada in', 60.34, 15, '2021-04-09 00:00:00', 6, '-'),
                        (260, 'Cheese - Brie, Triple Creme', 'tempus sit amet sem fusce consequat nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis enim', 17.75, 88, '2021-05-25 00:00:00', 4, '-'),
                        (261, 'Table Cloth 54x72 White', 'turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget', 44.88, 48, '2020-07-07 00:00:00', 4, '-'),
                        (262, 'Chocolate Bar - Oh Henry', 'in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu', 67.60, 99, '2020-07-16 00:00:00', 5, '-'),
                        (263, 'Cheese - Camembert', 'semper porta volutpat quam pede lobortis ligula sit amet eleifend', 23.20, 27, '2021-01-20 00:00:00', 5, '-'),
                        (264, 'Soup - Campbells, Spinach Crm', 'a odio in hac habitasse platea dictumst maecenas ut massa quis augue luctus tincidunt nulla', 31.98, 100, '2021-05-13 00:00:00', 3, '-'),
                        (265, 'Tea - Herbal Orange Spice', 'a nibh in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla', 80.89, 86, '2021-03-03 00:00:00', 5, '-'),
                        (266, 'Berry Brulee', 'praesent id massa id nisl venenatis lacinia aenean sit amet justo', 37.42, 5, '2021-05-21 00:00:00', 4, '-'),
                        (267, 'Bar - Sweet And Salty Chocolate', 'orci mauris lacinia sapien quis libero nullam sit amet turpis elementum ligula vehicula consequat morbi', 22.84, 26, '2020-12-21 00:00:00', 5, '-'),
                        (268, 'Gherkin', 'at nulla suspendisse potenti cras in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient montes', 57.02, 86, '2021-04-16 00:00:00', 4, '-'),
                        (269, 'Lady Fingers', 'vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet', 75.55, 59, '2020-08-07 00:00:00', 5, '-'),
                        (270, 'Beer - Upper Canada Light', 'maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum', 40.14, 56, '2020-12-07 00:00:00', 5, '-'),
                        (271, 'Cocoa Powder - Dutched', 'est congue elementum in hac habitasse platea dictumst morbi vestibulum velit', 13.36, 84, '2021-05-01 00:00:00', 4, '-'),
                        (272, 'Spice - Montreal Steak Spice', 'morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc rhoncus', 45.15, 81, '2020-11-29 00:00:00', 5, '-'),
                        (273, 'Jicama', 'in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor', 47.77, 92, '2021-03-29 00:00:00', 4, '-'),
                        (274, 'Bar Mix - Lime', 'sed vel enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper', 49.72, 80, '2020-10-10 00:00:00', 6, '-'),
                        (275, 'Macaroons - Two Bite Choc', 'rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed magna at', 80.59, 50, '2021-05-23 00:00:00', 5, '-'),
                        (276, 'Bandage - Fexible 1x3', 'nulla ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non', 63.84, 93, '2021-05-15 00:00:00', 6, '-'),
                        (277, 'V8 - Tropical Blend', 'in tempus sit amet sem fusce consequat nulla nisl nunc nisl duis bibendum felis sed interdum', 87.59, 70, '2020-12-29 00:00:00', 6, '-'),
                        (278, 'Yoplait Drink', 'tortor sollicitudin mi sit amet lobortis sapien sapien non mi integer ac neque duis bibendum morbi non', 59.28, 16, '2020-08-03 00:00:00', 4, '-'),
                        (279, 'Sugar - Invert', 'primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor', 69.37, 87, '2020-06-28 00:00:00', 5, '-'),
                        (280, 'Doilies - 10, Paper', 'mattis pulvinar nulla pede ullamcorper augue a suscipit nulla elit ac nulla', 99.19, 24, '2021-05-08 00:00:00', 4, '-'),
                        (281, 'Shrimp, Dried, Small / Lb', 'in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc donec', 24.32, 34, '2020-08-29 00:00:00', 3, '-'),
                        (282, 'Vinegar - Tarragon', 'auctor gravida sem praesent id massa id nisl venenatis lacinia aenean sit amet justo morbi ut odio', 16.87, 63, '2021-05-17 00:00:00', 5, '-'),
                        (283, 'Cheese - La Sauvagine', 'ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci luctus et', 82.33, 81, '2021-01-31 00:00:00', 3, '-'),
                        (284, 'Yucca', 'erat tortor sollicitudin mi sit amet lobortis sapien sapien non mi integer ac neque duis bibendum morbi non quam', 14.26, 67, '2020-10-19 00:00:00', 4, '-'),
                        (285, 'Beef - Shank', 'at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra', 18.74, 25, '2020-11-03 00:00:00', 4, '-'),
                        (286, 'Potatoes - Mini White 3 Oz', 'sed magna at nunc commodo placerat praesent blandit nam nulla integer pede justo lacinia', 4.00, 13, '2020-12-24 00:00:00', 5, '-'),
                        (287, 'Cup - 6oz, Foam', 'sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus', 2.83, 38, '2021-01-11 00:00:00', 5, '-'),
                        (288, 'Allspice - Jamaican', 'rhoncus aliquet pulvinar sed nisl nunc rhoncus dui vel sem sed sagittis', 46.53, 71, '2021-04-05 00:00:00', 4, '-'),
                        (289, 'Spice - Peppercorn Melange', 'ut rhoncus aliquet pulvinar sed nisl nunc rhoncus dui vel sem', 32.25, 8, '2021-02-24 00:00:00', 5, '-'),
                        (290, 'Ham Black Forest', 'a odio in hac habitasse platea dictumst maecenas ut massa quis augue luctus tincidunt nulla mollis molestie', 2.97, 68, '2020-12-13 00:00:00', 6, '-'),
                        (291, 'Chocolate - Chips Compound', 'interdum venenatis turpis enim blandit mi in porttitor pede justo eu massa donec dapibus duis at velit eu est', 10.59, 95, '2020-08-11 00:00:00', 5, '-'),
                        (292, 'Lamb - Shanks', 'accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam sit amet turpis elementum', 85.78, 91, '2021-05-30 00:00:00', 3, '-'),
                        (293, 'Wine - Chianti Classico Riserva', 'cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus vivamus vestibulum', 42.08, 82, '2021-01-20 00:00:00', 6, '-'),
                        (294, 'Coffee - Colombian, Portioned', 'felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed', 5.99, 48, '2020-08-15 00:00:00', 3, '-'),
                        (295, 'Pasta - Fettuccine, Egg, Fresh', 'sed accumsan felis ut at dolor quis odio consequat varius integer ac leo pellentesque ultrices mattis', 12.85, 16, '2020-06-12 00:00:00', 6, '-'),
                        (296, 'Tequila Rose Cream Liquor', 'molestie lorem quisque ut erat curabitur gravida nisi at nibh in hac', 94.35, 28, '2020-12-03 00:00:00', 3, '-'),
                        (297, 'Eggwhite Frozen', 'faucibus orci luctus et ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet ultrices erat', 64.40, 80, '2021-02-24 00:00:00', 5, '-'),
                        (298, 'Pate - Liver', 'sed tincidunt eu felis fusce posuere felis sed lacus morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc', 87.14, 86, '2021-03-26 00:00:00', 4, '-'),
                        (299, 'Thyme - Fresh', 'lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum primis', 13.95, 80, '2020-10-30 00:00:00', 5, '-'),
                        (300, 'Ice Cream - Strawberry', 'purus sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus at diam nam', 78.47, 75, '2020-11-13 00:00:00', 6, '-'),
                        (301, 'Steampan - Lid For Half Size', 'ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae mauris viverra diam vitae quam', 29.54, 95, '2020-07-30 00:00:00', 4, '-'),
                        (302, 'Oats Large Flake', 'fusce lacus purus aliquet at feugiat non pretium quis lectus suspendisse potenti in eleifend quam a odio', 99.60, 100, '2020-08-02 00:00:00', 3, '-'),
                        (303, 'Mcguinness - Blue Curacao', 'convallis eget eleifend luctus ultricies eu nibh quisque id justo sit amet sapien dignissim', 30.76, 42, '2020-08-22 00:00:00', 5, '-'),
                        (304, 'Sauce - Salsa', 'a nibh in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum', 82.29, 24, '2020-12-09 00:00:00', 5, '-'),
                        (305, 'Frangelico', 'ante ipsum primis in faucibus orci luctus et ultrices posuere', 8.45, 20, '2021-04-12 00:00:00', 5, '-'),
                        (306, 'Wine - Blue Nun Qualitatswein', 'neque aenean auctor gravida sem praesent id massa id nisl venenatis lacinia aenean sit amet justo', 67.43, 65, '2020-07-17 00:00:00', 4, '-'),
                        (307, 'Bread - Calabrese Baguette', 'est donec odio justo sollicitudin ut suscipit a feugiat et eros vestibulum ac est', 40.96, 5, '2020-11-04 00:00:00', 5, '-'),
                        (308, 'Soup - Campbells', 'nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit amet', 70.29, 81, '2021-05-08 00:00:00', 4, '-'),
                        (309, 'Doilies - 8, Paper', 'pretium iaculis diam erat fermentum justo nec condimentum neque sapien placerat ante nulla justo', 49.70, 80, '2021-04-30 00:00:00', 4, '-'),
                        (310, 'Taro Leaves', 'diam cras pellentesque volutpat dui maecenas tristique est et tempus', 64.75, 87, '2020-12-12 00:00:00', 5, '-'),
                        (311, 'Tumeric', 'volutpat erat quisque erat eros viverra eget congue eget semper rutrum', 17.35, 70, '2020-07-25 00:00:00', 6, '-'),
                        (312, 'Coconut - Creamed, Pure', 'justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet', 52.81, 80, '2021-03-02 00:00:00', 5, '-'),
                        (313, 'Bread - Olive Dinner Roll', 'ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet ultrices erat tortor', 88.96, 61, '2021-02-12 00:00:00', 3, '-'),
                        (314, 'Wine - Fat Bastard Merlot', 'nisi eu orci mauris lacinia sapien quis libero nullam sit amet turpis elementum ligula vehicula consequat morbi a ipsum integer', 73.55, 14, '2020-12-04 00:00:00', 3, '-'),
                        (315, 'Beef - Tenderloin', 'nibh in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo', 52.03, 10, '2020-08-02 00:00:00', 3, '-'),
                        (316, 'Bread - White Epi Baguette', 'morbi non lectus aliquam sit amet diam in magna bibendum imperdiet nullam orci pede venenatis non sodales sed tincidunt eu', 2.21, 48, '2021-05-03 00:00:00', 6, '-'),
                        (317, 'Soup - Campbells, Creamy', 'hac habitasse platea dictumst maecenas ut massa quis augue luctus', 14.16, 67, '2020-10-20 00:00:00', 3, '-'),
                        (318, 'Dasheen', 'donec dapibus duis at velit eu est congue elementum in hac habitasse', 33.04, 88, '2021-02-18 00:00:00', 3, '-'),
                        (319, 'Towel - Roll White', 'mauris morbi non lectus aliquam sit amet diam in magna bibendum imperdiet nullam orci', 36.51, 11, '2021-01-30 00:00:00', 6, '-'),
                        (320, 'Juice - Orange 1.89l', 'elit proin risus praesent lectus vestibulum quam sapien varius ut blandit', 85.16, 7, '2021-02-12 00:00:00', 3, '-'),
                        (321, 'Vermouth - White, Cinzano', 'molestie lorem quisque ut erat curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam augue', 46.15, 35, '2020-09-13 00:00:00', 5, '-'),
                        (322, 'Bread - French Baquette', 'mi in porttitor pede justo eu massa donec dapibus duis at velit eu est congue elementum in hac', 30.31, 38, '2020-08-24 00:00:00', 5, '-'),
                        (323, 'Chinese Foods - Plain Fried Rice', 'pulvinar lobortis est phasellus sit amet erat nulla tempus vivamus in felis eu sapien cursus vestibulum proin eu', 24.39, 6, '2021-02-07 00:00:00', 4, '-'),
                        (324, 'Sausage - Chorizo', 'magnis dis parturient montes nascetur ridiculus mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis', 72.17, 62, '2021-03-31 00:00:00', 6, '-'),
                        (325, 'Lotus Root', 'mi nulla ac enim in tempor turpis nec euismod scelerisque quam turpis', 16.48, 55, '2021-03-12 00:00:00', 3, '-'),
                        (326, 'Ecolab - Solid Fusion', 'at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate', 78.05, 98, '2021-03-17 00:00:00', 5, '-'),
                        (327, 'Chicken - Thigh, Bone In', 'nunc nisl duis bibendum felis sed interdum venenatis turpis enim blandit mi in porttitor pede justo eu', 61.95, 100, '2020-08-15 00:00:00', 6, '-'),
                        (328, 'Pepper - Red Chili', 'suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus', 5.21, 96, '2020-09-12 00:00:00', 4, '-'),
                        (329, 'Soup - Beef, Base Mix', 'amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac tellus', 41.99, 89, '2020-10-20 00:00:00', 6, '-'),
                        (330, 'Wine - Magnotta - Cab Franc', 'ut erat curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam augue quam', 13.21, 43, '2021-05-16 00:00:00', 6, '-'),
                        (331, 'Red Currant Jelly', 'at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat', 44.53, 95, '2020-07-08 00:00:00', 6, '-'),
                        (332, 'Soup - Knorr, Country Bean', 'consequat metus sapien ut nunc vestibulum ante ipsum primis in', 75.74, 54, '2021-02-20 00:00:00', 3, '-'),
                        (333, 'Cafe Royale', 'bibendum imperdiet nullam orci pede venenatis non sodales sed tincidunt eu felis fusce posuere felis sed lacus', 77.72, 73, '2021-01-27 00:00:00', 4, '-'),
                        (334, 'Napkin White', 'sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus at', 41.16, 75, '2021-05-24 00:00:00', 5, '-'),
                        (335, 'Cheese - Provolone', 'pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo etiam pretium iaculis justo in', 54.32, 19, '2021-02-04 00:00:00', 3, '-'),
                        (336, 'Vermacelli - Sprinkles, Assorted', 'id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus at', 33.79, 46, '2020-06-10 00:00:00', 6, '-'),
                        (337, 'Creme De Cacao White', 'condimentum neque sapien placerat ante nulla justo aliquam quis turpis eget elit sodales', 30.59, 29, '2020-10-29 00:00:00', 5, '-'),
                        (338, 'Mushroom - Lg - Cello', 'nec sem duis aliquam convallis nunc proin at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum', 29.11, 29, '2021-05-23 00:00:00', 4, '-'),
                        (339, 'Assorted Desserts', 'phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate', 16.77, 97, '2020-06-23 00:00:00', 6, '-'),
                        (340, 'Pork - Suckling Pig', 'nascetur ridiculus mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis', 76.52, 73, '2021-02-17 00:00:00', 4, '-'),
                        (341, 'Wine - Hardys Bankside Shiraz', 'dui vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non pretium quis lectus suspendisse potenti', 65.85, 72, '2020-10-04 00:00:00', 4, '-'),
                        (342, 'Tart Shells - Savory, 3', 'rutrum nulla tellus in sagittis dui vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non', 64.88, 44, '2020-08-26 00:00:00', 3, '-'),
                        (343, 'Cheese - Gouda', 'pretium quis lectus suspendisse potenti in eleifend quam a odio in hac habitasse platea dictumst maecenas ut massa quis', 98.07, 44, '2021-03-11 00:00:00', 4, '-'),
                        (344, 'Beef - Tenderloin - Aa', 'ligula sit amet eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque', 36.69, 9, '2020-11-28 00:00:00', 4, '-'),
                        (345, 'Pork - Ham, Virginia', 'consequat morbi a ipsum integer a nibh in quis justo maecenas', 58.53, 79, '2021-03-01 00:00:00', 6, '-'),
                        (346, 'Lid Tray - 16in Dome', 'accumsan tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean', 30.96, 32, '2021-01-29 00:00:00', 6, '-'),
                        (347, 'Beer - Corona', 'morbi a ipsum integer a nibh in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices', 93.68, 84, '2020-06-14 00:00:00', 5, '-'),
                        (348, 'Milkettes - 2%', 'dui luctus rutrum nulla tellus in sagittis dui vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non', 86.05, 64, '2020-09-23 00:00:00', 3, '-'),
                        (349, 'Five Alive Citrus', 'orci pede venenatis non sodales sed tincidunt eu felis fusce', 27.86, 59, '2021-05-12 00:00:00', 4, '-'),
                        (350, 'Pasta - Canelloni, Single Serve', 'nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum', 20.21, 19, '2020-08-27 00:00:00', 5, '-'),
                        (351, 'Juice - Cranberry 284ml', 'placerat praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget tempus vel pede', 13.05, 56, '2021-05-11 00:00:00', 5, '-'),
                        (352, 'Wine - Vineland Estate Semi - Dry', 'tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh quisque', 33.35, 71, '2021-05-18 00:00:00', 3, '-'),
                        (353, 'Syrup - Monin - Passion Fruit', 'non velit donec diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum', 64.58, 56, '2020-09-25 00:00:00', 5, '-'),
                        (354, 'Marsala - Sperone, Fine, D.o.c.', 'congue etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus', 71.21, 80, '2021-04-09 00:00:00', 4, '-'),
                        (355, 'Bowl 12 Oz - Showcase 92012', 'quis lectus suspendisse potenti in eleifend quam a odio in', 7.67, 33, '2020-07-20 00:00:00', 6, '-'),
                        (356, 'Cod - Salted, Boneless', 'est risus auctor sed tristique in tempus sit amet sem fusce consequat', 26.71, 12, '2020-07-28 00:00:00', 5, '-'),
                        (357, 'Lemonade - Kiwi, 591 Ml', 'tincidunt nulla mollis molestie lorem quisque ut erat curabitur gravida nisi at nibh in hac habitasse', 43.40, 41, '2020-10-11 00:00:00', 5, '-'),
                        (358, 'Yeast Dry - Fleischman', 'tellus nulla ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas', 44.77, 32, '2020-08-19 00:00:00', 4, '-'),
                        (359, 'Beef - Striploin', 'sapien non mi integer ac neque duis bibendum morbi non quam nec dui luctus', 77.01, 95, '2021-05-13 00:00:00', 4, '-'),
                        (360, 'Plate Pie Foil', 'lorem quisque ut erat curabitur gravida nisi at nibh in hac habitasse', 6.97, 84, '2020-08-05 00:00:00', 5, '-'),
                        (361, 'Madeira', 'maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus', 28.66, 89, '2020-11-30 00:00:00', 4, '-'),
                        (362, 'Broccoli - Fresh', 'morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc rhoncus', 84.58, 93, '2020-11-20 00:00:00', 4, '-'),
                        (363, 'Wine - Rubyport', 'turpis enim blandit mi in porttitor pede justo eu massa donec dapibus duis at velit eu', 98.70, 92, '2020-08-10 00:00:00', 4, '-'),
                        (364, 'Bread Base - Italian', 'lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi', 19.74, 28, '2021-06-03 00:00:00', 6, '-'),
                        (365, 'Flour - Corn, Fine', 'curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non mi integer', 32.55, 68, '2021-04-02 00:00:00', 5, '-'),
                        (366, 'Bread Cranberry Foccacia', 'nulla pede ullamcorper augue a suscipit nulla elit ac nulla sed', 95.08, 76, '2020-10-24 00:00:00', 3, '-'),
                        (367, 'Lettuce - Boston Bib - Organic', 'elit sodales scelerisque mauris sit amet eros suspendisse accumsan tortor quis turpis sed ante vivamus', 41.65, 31, '2021-03-17 00:00:00', 4, '-'),
                        (368, 'Beef - Tenderlion, Center Cut', 'quam suspendisse potenti nullam porttitor lacus at turpis donec posuere metus vitae ipsum aliquam non mauris morbi non lectus', 3.45, 36, '2020-09-08 00:00:00', 5, '-'),
                        (369, 'Squeeze Bottle', 'consequat metus sapien ut nunc vestibulum ante ipsum primis in faucibus orci luctus et ultrices', 75.90, 17, '2020-12-27 00:00:00', 5, '-'),
                        (370, 'Muffin - Zero Transfat', 'quis augue luctus tincidunt nulla mollis molestie lorem quisque ut erat curabitur gravida nisi at', 15.91, 65, '2020-07-21 00:00:00', 6, '-'),
                        (371, 'Worcestershire Sauce', 'cubilia curae mauris viverra diam vitae quam suspendisse potenti nullam porttitor lacus', 45.93, 61, '2020-12-06 00:00:00', 5, '-'),
                        (372, 'Lid Coffee Cup 8oz Blk', 'sit amet erat nulla tempus vivamus in felis eu sapien cursus', 52.14, 21, '2021-02-18 00:00:00', 3, '-'),
                        (373, 'Yoplait Drink', 'eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit', 20.55, 67, '2021-04-18 00:00:00', 6, '-'),
                        (374, 'Sausage - Liver', 'lacus at turpis donec posuere metus vitae ipsum aliquam non mauris morbi', 58.67, 39, '2020-10-20 00:00:00', 4, '-'),
                        (375, 'Snapple Lemon Tea', 'interdum mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie', 42.45, 43, '2020-11-02 00:00:00', 4, '-'),
                        (376, 'Salmon - Atlantic, No Skin', 'dis parturient montes nascetur ridiculus mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus', 38.85, 15, '2020-10-31 00:00:00', 3, '-'),
                        (377, 'Black Currants', 'accumsan tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean', 76.68, 63, '2020-09-21 00:00:00', 4, '-'),
                        (378, 'Food Colouring - Red', 'rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum', 52.70, 87, '2020-08-17 00:00:00', 4, '-'),
                        (379, 'Chocolate - White', 'id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam sit', 1.92, 69, '2021-04-02 00:00:00', 4, '-'),
                        (380, 'Calaloo', 'urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat', 8.55, 76, '2020-08-03 00:00:00', 5, '-'),
                        (381, 'Cherries - Fresh', 'nulla nunc purus phasellus in felis donec semper sapien a', 31.41, 45, '2020-09-04 00:00:00', 3, '-'),
                        (382, 'Muffin Orange Individual', 'justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec', 54.18, 13, '2020-07-09 00:00:00', 3, '-'),
                        (383, 'Soup - French Can Pea', 'sed ante vivamus tortor duis mattis egestas metus aenean fermentum donec ut mauris eget massa tempor convallis nulla', 76.57, 85, '2021-04-17 00:00:00', 4, '-'),
                        (384, 'Nectarines', 'arcu sed augue aliquam erat volutpat in congue etiam justo etiam pretium iaculis', 11.16, 30, '2020-10-26 00:00:00', 4, '-'),
                        (385, 'Shrimp - 21/25, Peel And Deviened', 'lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat', 68.55, 65, '2020-11-14 00:00:00', 5, '-'),
                        (386, 'Salmon - Smoked, Sliced', 'suspendisse potenti in eleifend quam a odio in hac habitasse platea dictumst maecenas ut massa quis augue luctus tincidunt nulla', 50.50, 100, '2021-03-27 00:00:00', 3, '-'),
                        (387, 'Quail - Jumbo Boneless', 'ligula vehicula consequat morbi a ipsum integer a nibh in quis justo maecenas rhoncus aliquam lacus', 20.37, 97, '2020-08-19 00:00:00', 4, '-'),
                        (388, 'Water - Spring Water, 355 Ml', 'diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci luctus et', 11.69, 75, '2021-02-04 00:00:00', 4, '-'),
                        (389, 'Pastry - Choclate Baked', 'purus phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in consequat', 70.65, 11, '2020-12-27 00:00:00', 3, '-'),
                        (390, 'Banana Turning', 'ligula sit amet eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque', 17.12, 36, '2020-12-24 00:00:00', 5, '-'),
                        (391, 'Flavouring Vanilla Artificial', 'sapien placerat ante nulla justo aliquam quis turpis eget elit sodales scelerisque mauris sit amet eros suspendisse accumsan tortor', 9.47, 59, '2021-01-21 00:00:00', 3, '-'),
                        (392, 'Lotus Rootlets - Canned', 'pede justo lacinia eget tincidunt eget tempus vel pede morbi', 72.76, 8, '2021-05-06 00:00:00', 5, '-'),
                        (393, 'Filter - Coffee', 'convallis morbi odio odio elementum eu interdum eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat', 85.17, 51, '2021-04-10 00:00:00', 4, '-'),
                        (394, 'Appetizer - Smoked Salmon / Dill', 'pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate', 32.16, 11, '2020-11-08 00:00:00', 5, '-'),
                        (395, 'Macaroons - Two Bite Choc', 'eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras', 68.07, 19, '2020-08-08 00:00:00', 3, '-'),
                        (396, 'Lamb - Bones', 'pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing', 36.67, 24, '2021-05-13 00:00:00', 6, '-'),
                        (397, 'Mousse - Mango', 'nunc commodo placerat praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem', 84.22, 91, '2020-08-03 00:00:00', 3, '-'),
                        (398, 'Truffle Shells - Semi - Sweet', 'maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus vivamus in felis eu sapien', 72.09, 19, '2020-08-17 00:00:00', 5, '-'),
                        (399, 'Pork - Tenderloin, Frozen', 'eu felis fusce posuere felis sed lacus morbi sem mauris', 52.90, 8, '2020-10-29 00:00:00', 4, '-'),
                        (400, 'Chilli Paste, Ginger Garlic', 'hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat id mauris vulputate elementum nullam', 50.47, 3, '2021-03-12 00:00:00', 3, '-'),
                        (401, 'Creme De Menth - White', 'in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc donec', 23.97, 49, '2021-01-05 00:00:00', 5, '-'),
                        (402, 'Thyme - Dried', 'semper interdum mauris ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis', 85.99, 96, '2020-11-26 00:00:00', 4, '-'),
                        (403, 'Pasta - Lasagna, Dry', 'eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien', 37.80, 49, '2020-11-12 00:00:00', 4, '-'),
                        (404, 'Eggplant Italian', 'lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque', 80.68, 52, '2021-05-13 00:00:00', 5, '-'),
                        (405, 'V8 - Vegetable Cocktail', 'ipsum integer a nibh in quis justo maecenas rhoncus aliquam lacus morbi', 26.62, 14, '2021-04-16 00:00:00', 3, '-'),
                        (406, 'Tray - 16in Rnd Blk', 'nisi nam ultrices libero non mattis pulvinar nulla pede ullamcorper augue a suscipit nulla elit', 20.69, 46, '2021-04-09 00:00:00', 6, '-'),
                        (407, 'Juice Peach Nectar', 'risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam sit', 47.08, 11, '2020-11-07 00:00:00', 4, '-'),
                        (408, 'Shrimp - Baby, Warm Water', 'magna bibendum imperdiet nullam orci pede venenatis non sodales sed tincidunt eu felis fusce posuere felis sed', 21.07, 14, '2021-04-10 00:00:00', 6, '-'),
                        (409, 'Chicken - Whole Fryers', 'ac lobortis vel dapibus at diam nam tristique tortor eu', 60.39, 59, '2020-09-25 00:00:00', 6, '-'),
                        (410, 'Gatorade - Orange', 'ridiculus mus etiam vel augue vestibulum rutrum rutrum neque aenean auctor gravida sem praesent id massa id nisl venenatis lacinia', 98.40, 58, '2020-11-18 00:00:00', 5, '-'),
                        (411, 'Fib N9 - Prague Powder', 'morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc rhoncus', 53.53, 91, '2020-11-21 00:00:00', 5, '-'),
                        (412, 'Mushroom - Enoki, Fresh', 'adipiscing lorem vitae mattis nibh ligula nec sem duis aliquam convallis nunc proin at', 39.73, 44, '2021-03-23 00:00:00', 5, '-'),
                        (413, 'Sauce - Hp', 'aliquet at feugiat non pretium quis lectus suspendisse potenti in eleifend quam a odio in hac habitasse platea', 57.26, 35, '2021-01-23 00:00:00', 4, '-'),
                        (414, 'Beer - Paulaner Hefeweisse', 'duis consequat dui nec nisi volutpat eleifend donec ut dolor', 95.30, 68, '2020-12-15 00:00:00', 3, '-'),
                        (415, 'Nut - Pecan, Halves', 'fusce posuere felis sed lacus morbi sem mauris laoreet ut rhoncus', 81.11, 48, '2021-05-16 00:00:00', 4, '-'),
                        (416, 'Vodka - Smirnoff', 'proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum primis', 24.05, 62, '2020-08-07 00:00:00', 3, '-'),
                        (417, 'Wine - Port Late Bottled Vintage', 'suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit amet nulla', 27.91, 95, '2021-04-25 00:00:00', 6, '-'),
                        (418, 'Kiwi Gold Zespri', 'id pretium iaculis diam erat fermentum justo nec condimentum neque sapien placerat ante nulla justo aliquam quis turpis eget', 28.83, 92, '2020-12-31 00:00:00', 3, '-'),
                        (419, 'Soup - Chicken And Wild Rice', 'primis in faucibus orci luctus et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis consequat dui', 74.76, 96, '2020-12-04 00:00:00', 5, '-'),
                        (420, 'Cream Of Tartar', 'suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum', 4.22, 42, '2021-02-15 00:00:00', 3, '-'),
                        (421, 'Pasta - Cheese / Spinach Bauletti', 'lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem id ligula suspendisse ornare', 81.91, 12, '2020-10-23 00:00:00', 3, '-'),
                        (422, 'Yucca', 'augue aliquam erat volutpat in congue etiam justo etiam pretium iaculis', 7.39, 34, '2020-09-13 00:00:00', 4, '-'),
                        (423, 'Zucchini - Yellow', 'in magna bibendum imperdiet nullam orci pede venenatis non sodales sed tincidunt eu felis', 55.25, 83, '2020-07-31 00:00:00', 6, '-'),
                        (424, 'Transfer Sheets', 'ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus', 91.43, 95, '2021-01-26 00:00:00', 6, '-'),
                        (425, 'Beef - Cooked, Corned', 'ut mauris eget massa tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh quisque id justo sit', 24.65, 65, '2021-01-02 00:00:00', 6, '-'),
                        (426, 'Bar Bran Honey Nut', 'ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla', 68.49, 30, '2021-04-14 00:00:00', 6, '-'),
                        (427, 'Quail - Whole, Bone - In', 'eros vestibulum ac est lacinia nisi venenatis tristique fusce congue diam id ornare', 41.85, 30, '2021-01-11 00:00:00', 6, '-'),
                        (428, 'Pepper - Julienne, Frozen', 'tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus', 22.56, 65, '2021-05-14 00:00:00', 5, '-'),
                        (429, 'Radish - Pickled', 'mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel', 91.52, 79, '2020-12-09 00:00:00', 5, '-'),
                        (430, 'Chocolate Eclairs', 'dictumst etiam faucibus cursus urna ut tellus nulla ut erat id mauris vulputate elementum nullam', 75.55, 30, '2021-05-11 00:00:00', 5, '-'),
                        (431, 'Godiva White Chocolate', 'velit id pretium iaculis diam erat fermentum justo nec condimentum neque sapien placerat ante nulla justo aliquam quis', 36.17, 73, '2020-09-08 00:00:00', 5, '-'),
                        (432, 'Sauce - Soya, Light', 'congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien', 81.10, 48, '2021-04-24 00:00:00', 6, '-'),
                        (433, 'Sherry - Dry', 'natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel augue', 78.54, 9, '2020-12-18 00:00:00', 5, '-'),
                        (434, 'Potatoes - Peeled', 'at turpis donec posuere metus vitae ipsum aliquam non mauris morbi non lectus aliquam sit amet diam', 82.59, 76, '2021-02-02 00:00:00', 6, '-'),
                        (435, 'Wine - Two Oceans Cabernet', 'nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum', 33.55, 86, '2020-10-16 00:00:00', 4, '-'),
                        (436, 'Appetizer - Southwestern', 'amet sem fusce consequat nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis enim blandit mi in porttitor', 38.94, 77, '2021-04-27 00:00:00', 4, '-'),
                        (437, 'Wine - Penfolds Koonuga Hill', 'luctus ultricies eu nibh quisque id justo sit amet sapien dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus', 50.05, 11, '2021-01-22 00:00:00', 5, '-'),
                        (438, 'Appetizer - Shrimp Puff', 'viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum', 65.45, 30, '2020-12-04 00:00:00', 4, '-'),
                        (439, 'Isomalt', 'sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel augue vestibulum', 33.57, 93, '2020-09-06 00:00:00', 5, '-'),
                        (440, 'Beans - Soya Bean', 'id turpis integer aliquet massa id lobortis convallis tortor risus', 88.40, 29, '2021-05-20 00:00:00', 4, '-'),
                        (441, 'Beef - Shank', 'volutpat in congue etiam justo etiam pretium iaculis justo in hac habitasse platea', 58.80, 99, '2020-10-19 00:00:00', 3, '-'),
                        (442, 'Oil - Shortening - All - Purpose', 'congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc donec', 15.47, 51, '2021-01-27 00:00:00', 3, '-'),
                        (443, 'Pepper - Chilli Seeds Mild', 'nisi volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla', 39.69, 35, '2020-10-03 00:00:00', 6, '-'),
                        (444, 'Pasta - Fusili, Dry', 'pretium iaculis diam erat fermentum justo nec condimentum neque sapien placerat ante', 17.95, 19, '2020-11-17 00:00:00', 3, '-'),
                        (445, 'Flower - Leather Leaf Fern', 'bibendum imperdiet nullam orci pede venenatis non sodales sed tincidunt eu felis fusce posuere felis sed lacus morbi sem', 69.96, 83, '2021-01-24 00:00:00', 5, '-'),
                        (446, 'Black Currants', 'lacus purus aliquet at feugiat non pretium quis lectus suspendisse', 8.73, 8, '2020-07-28 00:00:00', 6, '-'),
                        (447, 'Sword Pick Asst', 'ut massa quis augue luctus tincidunt nulla mollis molestie lorem quisque ut erat curabitur gravida nisi', 32.29, 16, '2021-01-21 00:00:00', 5, '-'),
                        (448, 'Soup - Campbells, Lentil', 'nascetur ridiculus mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam', 48.58, 76, '2021-01-27 00:00:00', 5, '-'),
                        (449, 'Roe - Lump Fish, Red', 'non mauris morbi non lectus aliquam sit amet diam in magna bibendum imperdiet nullam', 84.19, 65, '2021-04-04 00:00:00', 4, '-'),
                        (450, 'Sauce - Demi Glace', 'ante vivamus tortor duis mattis egestas metus aenean fermentum donec ut mauris eget massa', 81.03, 90, '2020-09-09 00:00:00', 4, '-'),
                        (451, 'Coffee Cup 8oz 5338cd', 'vestibulum ac est lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl', 73.11, 71, '2021-02-15 00:00:00', 6, '-'),
                        (452, 'Salmon - Smoked, Sliced', 'rutrum rutrum neque aenean auctor gravida sem praesent id massa id nisl venenatis lacinia aenean sit amet justo morbi', 30.55, 11, '2020-10-09 00:00:00', 4, '-'),
                        (453, 'Veal - Osso Bucco', 'ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo', 93.75, 23, '2020-10-31 00:00:00', 4, '-'),
                        (454, 'Sole - Dover, Whole, Fresh', 'nunc donec quis orci eget orci vehicula condimentum curabitur in libero', 14.14, 29, '2021-06-05 00:00:00', 6, '-'),
                        (455, 'Vaccum Bag - 14x20', 'libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed', 56.18, 92, '2021-03-26 00:00:00', 3, '-'),
                        (456, 'Sausage - Liver', 'adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum primis', 87.44, 25, '2020-08-01 00:00:00', 6, '-'),
                        (457, 'Wine - Magnotta, White', 'diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien', 96.03, 34, '2021-01-30 00:00:00', 5, '-'),
                        (458, 'Ham - Virginia', 'hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem', 93.87, 87, '2021-04-08 00:00:00', 4, '-'),
                        (459, 'Onion - Dried', 'semper porta volutpat quam pede lobortis ligula sit amet eleifend', 5.80, 5, '2020-09-24 00:00:00', 4, '-'),
                        (460, 'Coffee - Decafenated', 'mi sit amet lobortis sapien sapien non mi integer ac neque duis bibendum morbi non quam', 35.38, 32, '2020-09-29 00:00:00', 3, '-'),
                        (461, 'Sauce - Plum', 'platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat id mauris vulputate elementum nullam', 8.77, 35, '2020-07-03 00:00:00', 4, '-'),
                        (462, 'Yogurt - Raspberry, 175 Gr', 'habitasse platea dictumst morbi vestibulum velit id pretium iaculis diam erat fermentum justo nec condimentum neque', 74.58, 100, '2020-12-08 00:00:00', 4, '-'),
                        (463, 'Orange - Tangerine', 'ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae donec pharetra', 91.78, 85, '2020-06-19 00:00:00', 5, '-'),
                        (464, 'Chicken - Soup Base', 'nunc rhoncus dui vel sem sed sagittis nam congue risus semper porta volutpat quam pede lobortis ligula', 11.88, 55, '2020-08-20 00:00:00', 4, '-'),
                        (465, 'Ecolab - Lime - A - Way 4/4 L', 'nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum', 88.85, 93, '2021-05-27 00:00:00', 3, '-'),
                        (466, 'Cheese - Parmigiano Reggiano', 'morbi non lectus aliquam sit amet diam in magna bibendum imperdiet nullam orci pede venenatis non', 77.72, 82, '2020-08-17 00:00:00', 3, '-'),
                        (467, 'Beef - Chuck, Boneless', 'viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec', 85.88, 22, '2020-10-21 00:00:00', 5, '-'),
                        (468, 'Raisin - Golden', 'duis consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim', 94.29, 51, '2020-12-04 00:00:00', 4, '-'),
                        (469, 'Molasses - Fancy', 'ut odio cras mi pede malesuada in imperdiet et commodo vulputate', 1.13, 8, '2021-02-25 00:00:00', 3, '-'),
                        (470, 'Pork - Ground', 'vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non pretium quis lectus', 96.62, 34, '2020-07-19 00:00:00', 6, '-'),
                        (471, 'Bread - White, Unsliced', 'donec posuere metus vitae ipsum aliquam non mauris morbi non lectus aliquam sit amet diam in magna', 83.52, 51, '2021-01-17 00:00:00', 4, '-'),
                        (472, 'Versatainer Nc - 8288', 'dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia', 23.04, 81, '2020-07-13 00:00:00', 5, '-'),
                        (473, 'Lambcasing', 'nulla tempus vivamus in felis eu sapien cursus vestibulum proin eu mi nulla ac enim in', 78.97, 70, '2020-06-16 00:00:00', 6, '-'),
                        (474, 'Beef - Ox Tongue', 'augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat', 27.92, 79, '2020-11-05 00:00:00', 4, '-'),
                        (475, 'Pepper - Green, Chili', 'eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus vivamus in', 95.20, 61, '2021-01-13 00:00:00', 6, '-'),
                        (476, 'Beer - Tetleys', 'dapibus augue vel accumsan tellus nisi eu orci mauris lacinia', 34.41, 16, '2020-12-14 00:00:00', 3, '-'),
                        (477, 'Yogurt - Cherry, 175 Gr', 'phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut', 52.89, 80, '2020-08-05 00:00:00', 3, '-'),
                        (478, 'Sole - Fillet', 'interdum venenatis turpis enim blandit mi in porttitor pede justo eu massa donec dapibus duis at velit eu', 28.28, 35, '2021-04-26 00:00:00', 5, '-'),
                        (479, 'Turnip - White, Organic', 'sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus at diam nam tristique', 50.07, 25, '2021-02-09 00:00:00', 5, '-'),
                        (480, 'Dip - Tapenade', 'tellus in sagittis dui vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non pretium', 45.11, 41, '2020-08-11 00:00:00', 6, '-'),
                        (481, 'Coffee - 10oz Cup 92961', 'maecenas tincidunt lacus at velit vivamus vel nulla eget eros', 21.42, 93, '2021-05-01 00:00:00', 4, '-'),
                        (482, 'Pasta - Elbows, Macaroni, Dry', 'faucibus accumsan odio curabitur convallis duis consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus', 37.30, 87, '2021-04-08 00:00:00', 6, '-'),
                        (483, 'Wine - White, Colubia Cresh', 'lacinia sapien quis libero nullam sit amet turpis elementum ligula vehicula consequat morbi a', 1.59, 42, '2020-06-24 00:00:00', 4, '-'),
                        (484, 'Soup - Beef Conomme, Dry', 'ac enim in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis nibh ligula nec', 92.54, 75, '2021-01-05 00:00:00', 4, '-'),
                        (485, 'Soup - Campbells Mushroom', 'eu felis fusce posuere felis sed lacus morbi sem mauris laoreet ut rhoncus', 32.67, 17, '2020-09-27 00:00:00', 4, '-'),
                        (486, 'Potatoes - Mini Red', 'purus phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in', 57.24, 21, '2021-03-14 00:00:00', 5, '-'),
                        (487, 'Cheese - Havarti, Salsa', 'blandit non interdum in ante vestibulum ante ipsum primis in', 31.03, 75, '2020-12-06 00:00:00', 6, '-'),
                        (488, 'Shrimp - 21/25, Peel And Deviened', 'sed tristique in tempus sit amet sem fusce consequat nulla', 83.12, 20, '2020-07-09 00:00:00', 4, '-'),
                        (489, 'Propel Sport Drink', 'aliquam convallis nunc proin at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum', 50.37, 18, '2020-08-03 00:00:00', 4, '-'),
                        (490, 'Chicken - White Meat With Tender', 'vestibulum sit amet cursus id turpis integer aliquet massa id lobortis convallis', 39.47, 64, '2020-12-23 00:00:00', 6, '-'),
                        (491, 'Guinea Fowl', 'erat fermentum justo nec condimentum neque sapien placerat ante nulla justo aliquam quis turpis', 84.54, 43, '2020-11-04 00:00:00', 5, '-'),
                        (492, 'Bowl 12 Oz - Showcase 92012', 'praesent blandit lacinia erat vestibulum sed magna at nunc commodo', 29.71, 13, '2021-02-04 00:00:00', 4, '-'),
                        (493, 'Yeast Dry - Fermipan', 'libero ut massa volutpat convallis morbi odio odio elementum eu interdum eu tincidunt in leo', 10.79, 86, '2021-05-11 00:00:00', 3, '-'),
                        (494, 'Mushroom - Chantrelle, Fresh', 'amet eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras', 23.61, 39, '2020-09-12 00:00:00', 5, '-'),
                        (495, 'Beer - Steamwhistle', 'sagittis nam congue risus semper porta volutpat quam pede lobortis ligula sit', 7.39, 82, '2021-03-12 00:00:00', 4, '-'),
                        (496, 'Lettuce - Belgian Endive', 'libero quis orci nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate', 40.96, 59, '2020-09-30 00:00:00', 3, '-'),
                        (497, 'Jello - Assorted', 'in libero ut massa volutpat convallis morbi odio odio elementum eu interdum eu', 13.53, 97, '2021-02-22 00:00:00', 5, '-'),
                        (498, 'Garlic Powder', 'morbi vestibulum velit id pretium iaculis diam erat fermentum justo nec', 2.19, 3, '2020-08-27 00:00:00', 6, '-'),
                        (499, 'Pickle - Dill', 'sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam', 31.52, 77, '2020-09-20 00:00:00', 6, '-'),
                        (500, 'Flour Dark Rye', 'at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate ut ultrices vel', 37.41, 75, '2020-10-22 00:00:00', 5, '-'),
                        (501, 'Compound - Pear', 'potenti cras in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus', 93.42, 51, '2021-06-07 00:00:00', 6, '-'),
                        (502, 'Cookie Chocolate Chip With', 'libero convallis eget eleifend luctus ultricies eu nibh quisque id justo sit amet', 66.30, 29, '2020-07-25 00:00:00', 3, '-'),
                        (503, 'Cloves - Ground', 'nulla nunc purus phasellus in felis donec semper sapien a libero', 26.06, 15, '2020-11-08 00:00:00', 5, '-'),
                        (504, 'Sauce - Thousand Island', 'congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a', 60.11, 46, '2020-09-27 00:00:00', 4, '-'),
                        (505, 'Yogurt - Assorted Pack', 'suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum', 12.44, 67, '2020-07-25 00:00:00', 3, '-'),
                        (506, 'Dooleys Toffee', 'hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla', 71.19, 52, '2021-05-26 00:00:00', 6, '-'),
                        (507, 'Marzipan 50/50', 'felis fusce posuere felis sed lacus morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc rhoncus', 89.05, 58, '2021-03-25 00:00:00', 3, '-'),
                        (508, 'Flavouring - Raspberry', 'tincidunt eget tempus vel pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est', 72.89, 40, '2021-02-28 00:00:00', 6, '-'),
                        (509, 'Lamb - Bones', 'aenean lectus pellentesque eget nunc donec quis orci eget orci vehicula condimentum curabitur in libero ut massa', 1.44, 80, '2021-04-09 00:00:00', 5, '-'),
                        (510, 'Pineapple - Canned, Rings', 'aliquam sit amet diam in magna bibendum imperdiet nullam orci pede venenatis non sodales sed', 14.96, 77, '2021-04-04 00:00:00', 3, '-'),
                        (511, 'Chicken - Whole Roasting', 'sagittis nam congue risus semper porta volutpat quam pede lobortis ligula', 54.87, 44, '2021-02-10 00:00:00', 4, '-'),
                        (512, 'Scallops - U - 10', 'blandit non interdum in ante vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae', 88.21, 100, '2021-04-25 00:00:00', 4, '-'),
                        (513, 'Container - Clear 32 Oz', 'quis augue luctus tincidunt nulla mollis molestie lorem quisque ut erat curabitur gravida nisi at nibh in hac habitasse platea', 5.78, 30, '2021-03-04 00:00:00', 6, '-'),
                        (514, 'Juice - Orange 1.89l', 'eu mi nulla ac enim in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis', 54.45, 65, '2020-10-04 00:00:00', 4, '-'),
                        (515, 'Sparkling Wine - Rose, Freixenet', 'justo sollicitudin ut suscipit a feugiat et eros vestibulum ac est lacinia nisi venenatis tristique fusce congue', 95.18, 44, '2020-12-24 00:00:00', 3, '-'),
                        (516, 'Sultanas', 'maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum', 48.75, 64, '2020-08-27 00:00:00', 3, '-'),
                        (517, 'Pasta - Cheese / Spinach Bauletti', 'primis in faucibus orci luctus et ultrices posuere cubilia curae donec', 93.85, 21, '2021-03-28 00:00:00', 4, '-'),
                        (518, 'Tart - Pecan Butter Squares', 'ultrices posuere cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin', 4.75, 43, '2021-04-23 00:00:00', 4, '-'),
                        (519, 'Tarts Assorted', 'pulvinar nulla pede ullamcorper augue a suscipit nulla elit ac nulla', 68.34, 87, '2021-04-21 00:00:00', 6, '-'),
                        (520, 'Appetizer - Asian Shrimp Roll', 'massa id lobortis convallis tortor risus dapibus augue vel accumsan', 92.58, 47, '2021-03-15 00:00:00', 6, '-'),
                        (521, 'Pork - Smoked Back Bacon', 'primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin', 14.00, 1, '2021-05-13 00:00:00', 5, '-'),
                        (522, 'Vodka - Smirnoff', 'justo morbi ut odio cras mi pede malesuada in imperdiet et commodo vulputate justo in', 66.15, 38, '2020-09-15 00:00:00', 4, '-'),
                        (523, 'Cake - Miini Cheesecake Cherry', 'potenti nullam porttitor lacus at turpis donec posuere metus vitae ipsum aliquam non', 57.35, 37, '2020-11-19 00:00:00', 6, '-'),
                        (524, 'Tia Maria', 'dapibus duis at velit eu est congue elementum in hac habitasse platea dictumst morbi vestibulum velit id pretium iaculis diam', 57.76, 82, '2021-01-29 00:00:00', 6, '-'),
                        (525, 'Banana Turning', 'augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam sit amet turpis elementum', 90.39, 64, '2020-07-10 00:00:00', 6, '-'),
                        (526, 'Rice - Brown', 'eget vulputate ut ultrices vel augue vestibulum ante ipsum primis', 57.03, 54, '2020-10-04 00:00:00', 5, '-'),
                        (527, 'Potatoes - Fingerling 4 Oz', 'commodo placerat praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem', 32.99, 89, '2021-02-07 00:00:00', 6, '-'),
                        (528, 'Shrimp - Tiger 21/25', 'fermentum justo nec condimentum neque sapien placerat ante nulla justo aliquam quis turpis eget elit sodales scelerisque mauris', 79.68, 71, '2021-03-27 00:00:00', 6, '-'),
                        (529, 'Lamb - Shanks', 'proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum primis in faucibus', 17.39, 29, '2020-07-01 00:00:00', 6, '-'),
                        (530, 'Wine - Red, Cabernet Merlot', 'platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum', 89.73, 57, '2020-12-11 00:00:00', 4, '-'),
                        (531, 'Bread - Sour Batard', 'mauris non ligula pellentesque ultrices phasellus id sapien in sapien', 57.33, 6, '2021-05-04 00:00:00', 3, '-'),
                        (532, 'Ginger - Crystalized', 'turpis adipiscing lorem vitae mattis nibh ligula nec sem duis aliquam convallis nunc proin at turpis a', 8.17, 88, '2020-08-25 00:00:00', 3, '-'),
                        (533, 'Eggplant - Asian', 'lectus in est risus auctor sed tristique in tempus sit amet sem', 50.50, 69, '2020-12-26 00:00:00', 3, '-'),
                        (534, 'Wine - Malbec Trapiche Reserve', 'dapibus duis at velit eu est congue elementum in hac habitasse platea dictumst', 90.41, 61, '2020-11-10 00:00:00', 5, '-'),
                        (535, 'Coffee Cup 16oz Foam', 'justo lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est risus', 2.94, 82, '2021-02-04 00:00:00', 6, '-'),
                        (536, 'Coconut Milk - Unsweetened', 'ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo etiam', 66.22, 90, '2020-11-09 00:00:00', 6, '-'),
                        (537, 'Squid Ink', 'suspendisse potenti nullam porttitor lacus at turpis donec posuere metus vitae ipsum aliquam', 32.21, 65, '2020-06-20 00:00:00', 3, '-'),
                        (538, 'Wine - Bouchard La Vignee Pinot', 'habitasse platea dictumst morbi vestibulum velit id pretium iaculis diam erat fermentum justo nec condimentum', 90.55, 70, '2020-06-24 00:00:00', 6, '-'),
                        (539, 'Guinea Fowl', 'nonummy maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque', 4.85, 97, '2020-08-02 00:00:00', 3, '-'),
                        (540, 'Remy Red', 'justo morbi ut odio cras mi pede malesuada in imperdiet et commodo vulputate', 67.10, 41, '2021-04-05 00:00:00', 6, '-'),
                        (541, 'Cookie Dough - Chocolate Chip', 'erat fermentum justo nec condimentum neque sapien placerat ante nulla justo', 16.48, 11, '2020-09-09 00:00:00', 3, '-'),
                        (542, 'Fennel', 'non ligula pellentesque ultrices phasellus id sapien in sapien iaculis', 2.73, 15, '2021-01-15 00:00:00', 4, '-'),
                        (543, 'Nacho Chips', 'massa tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh', 57.42, 97, '2021-04-09 00:00:00', 6, '-'),
                        (544, 'Sugar - Invert', 'eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient montes', 23.54, 77, '2020-12-25 00:00:00', 6, '-'),
                        (545, 'Tarts Assorted', 'vitae ipsum aliquam non mauris morbi non lectus aliquam sit amet diam in magna', 79.79, 51, '2020-11-02 00:00:00', 3, '-'),
                        (546, 'Mushroom Morel Fresh', 'in congue etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla', 27.00, 52, '2020-10-21 00:00:00', 3, '-'),
                        (547, 'Hersey Shakes', 'sem fusce consequat nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis', 47.61, 23, '2020-12-19 00:00:00', 6, '-'),
                        (548, 'Tomatoes - Heirloom', 'semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero nam dui proin', 74.60, 84, '2021-01-14 00:00:00', 5, '-'),
                        (549, 'Tea - Herbal Orange Spice', 'vel pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est risus auctor sed tristique in', 68.15, 1, '2021-04-13 00:00:00', 3, '-'),
                        (550, 'Pork - Bacon Cooked Slcd', 'nonummy integer non velit donec diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus', 2.24, 94, '2020-09-04 00:00:00', 6, '-'),
                        (551, 'Mint - Fresh', 'rhoncus sed vestibulum sit amet cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue', 84.18, 45, '2020-10-01 00:00:00', 5, '-'),
                        (552, 'Bread - Bistro Sour', 'nibh in hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer', 99.35, 69, '2021-01-13 00:00:00', 3, '-'),
                        (553, 'Wine - Magnotta - Red, Baco', 'vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet ultrices', 27.60, 71, '2021-02-14 00:00:00', 5, '-'),
                        (554, 'Chicken - Leg, Fresh', 'leo odio condimentum id luctus nec molestie sed justo pellentesque viverra pede ac diam', 11.50, 2, '2021-06-02 00:00:00', 4, '-'),
                        (555, 'Soup - French Onion, Dry', 'libero non mattis pulvinar nulla pede ullamcorper augue a suscipit nulla elit ac nulla sed vel enim sit amet nunc', 66.46, 37, '2021-01-24 00:00:00', 6, '-'),
                        (556, 'Sachet', 'faucibus cursus urna ut tellus nulla ut erat id mauris', 74.35, 81, '2021-03-21 00:00:00', 3, '-'),
                        (557, 'Carrots - Purple, Organic', 'eu interdum eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus vivamus in felis', 12.34, 48, '2021-06-02 00:00:00', 5, '-'),
                        (558, 'Yogurt - Raspberry, 175 Gr', 'sodales sed tincidunt eu felis fusce posuere felis sed lacus morbi sem mauris laoreet', 73.13, 32, '2021-05-07 00:00:00', 6, '-'),
                        (559, 'Chocolate - Chips Compound', 'consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim', 91.36, 13, '2020-11-17 00:00:00', 4, '-'),
                        (560, 'Sponge Cake Mix - Chocolate', 'aliquet pulvinar sed nisl nunc rhoncus dui vel sem sed sagittis nam congue risus semper porta volutpat quam pede', 77.66, 75, '2020-07-28 00:00:00', 4, '-'),
                        (561, 'Flower - Potmums', 'justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat id', 62.42, 82, '2020-09-22 00:00:00', 5, '-'),
                        (562, 'Glass Clear 7 Oz Xl', 'sed lacus morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc rhoncus', 97.10, 97, '2020-11-03 00:00:00', 4, '-'),
                        (563, 'Flour - Strong Pizza', 'justo morbi ut odio cras mi pede malesuada in imperdiet et commodo', 2.22, 15, '2020-08-01 00:00:00', 6, '-'),
                        (564, 'Glass Clear 7 Oz Xl', 'tellus nulla ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit', 45.75, 85, '2020-09-28 00:00:00', 5, '-'),
                        (565, 'Taro Leaves', 'rutrum nulla nunc purus phasellus in felis donec semper sapien a libero', 56.91, 58, '2020-12-01 00:00:00', 3, '-'),
                        (566, 'Bread Bowl Plain', 'eu nibh quisque id justo sit amet sapien dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et', 11.53, 77, '2021-04-04 00:00:00', 5, '-'),
                        (567, 'Cheese - Cambozola', 'nibh fusce lacus purus aliquet at feugiat non pretium quis lectus suspendisse potenti in eleifend', 52.08, 44, '2020-07-02 00:00:00', 6, '-'),
                        (568, 'Lettuce - Spring Mix', 'dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla', 14.24, 50, '2020-08-29 00:00:00', 5, '-'),
                        (569, 'Crab - Claws, 26 - 30', 'congue risus semper porta volutpat quam pede lobortis ligula sit amet eleifend pede libero', 60.21, 78, '2021-02-22 00:00:00', 3, '-'),
                        (570, 'Stock - Chicken, White', 'velit eu est congue elementum in hac habitasse platea dictumst', 48.55, 24, '2021-04-15 00:00:00', 6, '-'),
                        (571, 'Latex Rubber Gloves Size 9', 'proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum', 1.13, 44, '2021-01-19 00:00:00', 3, '-'),
                        (572, 'Wine - White Cab Sauv.on', 'amet turpis elementum ligula vehicula consequat morbi a ipsum integer a nibh in', 34.66, 27, '2020-12-06 00:00:00', 6, '-'),
                        (573, 'Cheese - Brie, Cups 125g', 'nisl aenean lectus pellentesque eget nunc donec quis orci eget orci vehicula condimentum curabitur', 36.30, 32, '2020-06-12 00:00:00', 5, '-'),
                        (574, 'Flour - All Purpose', 'faucibus orci luctus et ultrices posuere cubilia curae mauris viverra diam', 5.11, 41, '2021-03-28 00:00:00', 4, '-'),
                        (575, 'Lemon Balm - Fresh', 'quis orci eget orci vehicula condimentum curabitur in libero ut massa volutpat convallis morbi odio odio', 24.68, 64, '2021-04-24 00:00:00', 3, '-'),
                        (576, 'Tomatoes - Roma', 'congue elementum in hac habitasse platea dictumst morbi vestibulum velit id pretium', 10.38, 89, '2020-07-05 00:00:00', 4, '-'),
                        (577, 'Soup - Campbells, Classic Chix', 'eu sapien cursus vestibulum proin eu mi nulla ac enim in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem', 24.59, 48, '2020-12-10 00:00:00', 5, '-'),
                        (578, 'Beer - Upper Canada Light', 'erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper', 98.21, 66, '2020-10-11 00:00:00', 4, '-'),
                        (579, 'Hersey Shakes', 'at nulla suspendisse potenti cras in purus eu magna vulputate luctus', 79.61, 74, '2020-09-16 00:00:00', 5, '-'),
                        (580, 'Extract - Rum', 'lobortis ligula sit amet eleifend pede libero quis orci nullam molestie nibh in', 23.37, 62, '2021-03-02 00:00:00', 3, '-'),
                        (581, 'Yams', 'elit ac nulla sed vel enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum', 12.88, 40, '2020-10-05 00:00:00', 4, '-'),
                        (582, 'Water - Spring 1.5lit', 'vestibulum sit amet cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan', 99.96, 49, '2021-03-18 00:00:00', 4, '-'),
                        (583, 'Skirt - 24 Foot', 'eget elit sodales scelerisque mauris sit amet eros suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis', 92.67, 7, '2021-03-20 00:00:00', 5, '-'),
                        (584, 'Flour Dark Rye', 'nibh quisque id justo sit amet sapien dignissim vestibulum vestibulum ante ipsum primis in', 52.70, 69, '2020-08-17 00:00:00', 6, '-'),
                        (585, 'Coffee - Almond Amaretto', 'lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna', 97.09, 82, '2020-09-17 00:00:00', 4, '-'),
                        (586, 'Bread - Rolls, Rye', 'erat nulla tempus vivamus in felis eu sapien cursus vestibulum proin eu mi', 80.76, 76, '2021-02-01 00:00:00', 4, '-'),
                        (587, 'Salmon - Fillets', 'euismod scelerisque quam turpis adipiscing lorem vitae mattis nibh ligula nec sem duis aliquam convallis nunc proin at turpis', 68.90, 8, '2021-03-12 00:00:00', 3, '-'),
                        (588, 'Cheese - Brick With Onion', 'nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit amet nulla', 52.21, 63, '2020-07-31 00:00:00', 6, '-'),
                        (589, 'Tray - 16in Rnd Blk', 'libero ut massa volutpat convallis morbi odio odio elementum eu interdum eu tincidunt in leo maecenas pulvinar lobortis', 32.03, 89, '2021-04-15 00:00:00', 5, '-'),
                        (590, 'Pike - Frozen Fillet', 'consequat nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis enim blandit mi in porttitor pede', 6.97, 5, '2021-01-12 00:00:00', 3, '-'),
                        (591, 'Kirsch - Schloss', 'dui vel nisl duis ac nibh fusce lacus purus aliquet at feugiat', 42.90, 44, '2021-03-09 00:00:00', 6, '-'),
                        (592, 'Ham - Procutinni', 'ante nulla justo aliquam quis turpis eget elit sodales scelerisque mauris sit amet eros suspendisse accumsan tortor', 41.48, 56, '2020-08-29 00:00:00', 5, '-'),
                        (593, 'Lettuce - Curly Endive', 'lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit', 2.38, 74, '2020-10-14 00:00:00', 4, '-'),
                        (594, 'Black Currants', 'morbi non quam nec dui luctus rutrum nulla tellus in sagittis dui vel nisl duis ac nibh fusce lacus purus', 17.39, 52, '2021-05-24 00:00:00', 6, '-'),
                        (595, 'Doilies - 5, Paper', 'vestibulum rutrum rutrum neque aenean auctor gravida sem praesent id massa id nisl venenatis lacinia aenean sit amet justo morbi', 1.06, 86, '2020-07-15 00:00:00', 6, '-'),
                        (596, 'Gelatine Powder', 'congue elementum in hac habitasse platea dictumst morbi vestibulum velit id pretium iaculis diam erat', 60.24, 100, '2020-08-11 00:00:00', 6, '-'),
                        (597, 'Noodles - Steamed Chow Mein', 'venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed', 10.56, 49, '2021-03-02 00:00:00', 5, '-'),
                        (598, 'Yogurt - Raspberry, 175 Gr', 'mi integer ac neque duis bibendum morbi non quam nec dui luctus rutrum nulla tellus in sagittis dui vel', 9.79, 35, '2020-09-23 00:00:00', 4, '-'),
                        (599, 'Tarts Assorted', 'neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci luctus', 84.04, 27, '2020-09-04 00:00:00', 4, '-'),
                        (600, 'Icecream - Dstk Super Cone', 'pede lobortis ligula sit amet eleifend pede libero quis orci', 50.84, 96, '2020-11-30 00:00:00', 3, '-'),
                        (601, 'Wine - Rhine Riesling Wolf Blass', 'ultrices mattis odio donec vitae nisi nam ultrices libero non mattis pulvinar nulla pede ullamcorper augue', 11.87, 17, '2021-04-27 00:00:00', 3, '-'),
                        (602, 'Beans - Fine', 'sit amet eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque at nulla', 54.25, 84, '2021-01-09 00:00:00', 4, '-'),
                        (603, 'Wine - Cousino Macul Antiguas', 'purus sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus', 33.22, 48, '2020-12-12 00:00:00', 4, '-'),
                        (604, 'Appetizer - Sausage Rolls', 'luctus et ultrices posuere cubilia curae mauris viverra diam vitae', 91.63, 13, '2020-06-18 00:00:00', 6, '-'),
                        (605, 'Russian Prince', 'donec posuere metus vitae ipsum aliquam non mauris morbi non lectus aliquam sit amet diam', 72.46, 49, '2020-08-25 00:00:00', 6, '-'),
                        (606, 'Cabbage - Nappa', 'quisque ut erat curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam augue quam sollicitudin vitae', 74.35, 2, '2021-04-13 00:00:00', 4, '-'),
                        (607, 'Syrup - Monin - Passion Fruit', 'quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec', 14.17, 55, '2020-06-10 00:00:00', 4, '-'),
                        (608, 'Jack Daniels', 'vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla', 63.09, 30, '2020-10-25 00:00:00', 4, '-'),
                        (609, 'Beef - Ground, Extra Lean, Fresh', 'mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at', 88.73, 35, '2021-04-12 00:00:00', 6, '-'),
                        (610, 'Icecream - Dstk Cml And Fdg', 'ut suscipit a feugiat et eros vestibulum ac est lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien', 78.11, 81, '2020-11-13 00:00:00', 3, '-'),
                        (611, 'Beer - Muskoka Cream Ale', 'diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat', 95.62, 10, '2021-02-15 00:00:00', 5, '-'),
                        (612, 'Wine - Acient Coast Caberne', 'massa id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia', 86.89, 7, '2020-10-04 00:00:00', 6, '-'),
                        (613, 'Shrimp - Baby, Warm Water', 'nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis enim blandit mi', 37.16, 33, '2020-07-26 00:00:00', 5, '-'),
                        (614, 'Quiche Assorted', 'sed augue aliquam erat volutpat in congue etiam justo etiam pretium iaculis justo in hac', 25.19, 57, '2021-05-03 00:00:00', 6, '-'),
                        (615, 'Appetizer - Sausage Rolls', 'rhoncus sed vestibulum sit amet cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan', 93.60, 94, '2021-04-02 00:00:00', 4, '-'),
                        (616, 'Ecolab - Ster Bac', 'donec semper sapien a libero nam dui proin leo odio porttitor id consequat', 93.16, 79, '2020-12-05 00:00:00', 6, '-'),
                        (617, 'Olives - Black, Pitted', 'ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel est', 67.08, 76, '2021-06-04 00:00:00', 3, '-'),
                        (618, 'Napkin - Beverge, White 2 - Ply', 'non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu', 73.73, 36, '2020-11-27 00:00:00', 4, '-'),
                        (619, 'Wine - Charddonnay Errazuriz', 'faucibus orci luctus et ultrices posuere cubilia curae mauris viverra diam vitae quam suspendisse potenti nullam', 16.29, 33, '2020-09-02 00:00:00', 5, '-'),
                        (620, 'Oil - Safflower', 'orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel', 7.67, 95, '2021-06-08 00:00:00', 4, '-'),
                        (621, 'Bread - Dark Rye', 'pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat', 65.31, 77, '2021-05-31 00:00:00', 6, '-'),
                        (622, 'Ginger - Ground', 'ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae', 71.12, 14, '2020-07-12 00:00:00', 3, '-'),
                        (623, 'Cucumber - English', 'cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin ut suscipit a feugiat et', 82.68, 68, '2021-01-19 00:00:00', 5, '-'),
                        (624, 'Sterno - Chafing Dish Fuel', 'mauris eget massa tempor convallis nulla neque libero convallis eget eleifend luctus', 52.77, 48, '2021-01-20 00:00:00', 4, '-'),
                        (625, 'Soup - Knorr, Chicken Noodle', 'ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel est donec', 50.07, 30, '2021-04-23 00:00:00', 3, '-'),
                        (626, 'Rum - Light, Captain Morgan', 'tellus in sagittis dui vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non', 90.20, 52, '2020-11-17 00:00:00', 5, '-'),
                        (627, 'Wine - Zinfandel California 2002', 'hac habitasse platea dictumst morbi vestibulum velit id pretium iaculis diam erat fermentum justo nec condimentum', 55.71, 38, '2020-07-04 00:00:00', 4, '-'),
                        (628, 'Pasta - Linguini, Dry', 'ac consequat metus sapien ut nunc vestibulum ante ipsum primis in faucibus', 78.66, 35, '2020-09-30 00:00:00', 4, '-'),
                        (629, 'Juice Peach Nectar', 'elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper', 25.05, 66, '2020-06-21 00:00:00', 3, '-'),
                        (630, 'Beef - Roasted, Cooked', 'eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper', 81.59, 13, '2021-02-13 00:00:00', 4, '-'),
                        (631, 'Icecream Cone - Areo Chocolate', 'vitae ipsum aliquam non mauris morbi non lectus aliquam sit amet diam in magna bibendum imperdiet nullam', 82.33, 89, '2020-09-14 00:00:00', 5, '-'),
                        (632, 'Wine - Maipo Valle Cabernet', 'eget nunc donec quis orci eget orci vehicula condimentum curabitur', 16.52, 92, '2020-06-14 00:00:00', 3, '-'),
                        (633, 'Lamb Rack Frenched Australian', 'et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis consequat', 95.50, 12, '2021-01-07 00:00:00', 4, '-'),
                        (634, 'Wine - Spumante Bambino White', 'praesent blandit lacinia erat vestibulum sed magna at nunc commodo placerat', 99.09, 30, '2021-02-06 00:00:00', 5, '-'),
                        (635, 'Sauce - White, Mix', 'ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis consequat dui', 90.02, 54, '2021-05-22 00:00:00', 3, '-'),
                        (636, 'Calypso - Black Cherry Lemonade', 'nullam orci pede venenatis non sodales sed tincidunt eu felis fusce', 28.12, 42, '2021-01-12 00:00:00', 5, '-'),
                        (637, 'Flour - Strong Pizza', 'rhoncus sed vestibulum sit amet cursus id turpis integer aliquet massa id lobortis convallis tortor', 10.05, 85, '2021-04-15 00:00:00', 6, '-'),
                        (638, 'Ecolab - Hand Soap Form Antibac', 'nisl venenatis lacinia aenean sit amet justo morbi ut odio cras mi pede malesuada in imperdiet et', 89.15, 74, '2021-05-31 00:00:00', 4, '-'),
                        (639, 'Nori Sea Weed', 'imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo etiam', 82.66, 91, '2021-03-05 00:00:00', 6, '-'),
                        (640, 'Bread - Calabrese Baguette', 'ac nulla sed vel enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac', 25.38, 43, '2020-10-03 00:00:00', 5, '-'),
                        (641, 'Tea - Earl Grey', 'nibh ligula nec sem duis aliquam convallis nunc proin at turpis a pede posuere', 95.08, 31, '2020-09-13 00:00:00', 3, '-'),
                        (642, 'Capicola - Hot', 'ac est lacinia nisi venenatis tristique fusce congue diam id', 90.60, 55, '2020-06-27 00:00:00', 3, '-'),
                        (643, 'Chinese Foods - Chicken', 'sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan felis ut', 4.77, 76, '2020-12-19 00:00:00', 6, '-'),
                        (644, 'Bread - French Stick', 'convallis morbi odio odio elementum eu interdum eu tincidunt in leo maecenas pulvinar lobortis est phasellus', 94.19, 21, '2021-04-02 00:00:00', 5, '-'),
                        (645, 'Sprouts - Onion', 'nunc proin at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget', 80.48, 64, '2020-07-06 00:00:00', 5, '-'),
                        (646, 'Pastry - French Mini Assorted', 'lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat', 53.14, 42, '2020-10-31 00:00:00', 6, '-'),
                        (647, 'Star Anise, Whole', 'luctus et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur', 23.01, 78, '2020-06-13 00:00:00', 5, '-'),
                        (648, '7up Diet, 355 Ml', 'tincidunt eget tempus vel pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est', 79.07, 82, '2020-07-16 00:00:00', 5, '-'),
                        (649, 'Rabbit - Saddles', 'cubilia curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non', 93.25, 69, '2021-02-08 00:00:00', 4, '-'),
                        (650, 'Sour Puss - Tangerine', 'cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci mauris', 40.35, 89, '2021-01-11 00:00:00', 6, '-'),
                        (651, 'Potato - Sweet', 'et ultrices posuere cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin', 85.45, 82, '2021-02-12 00:00:00', 4, '-'),
                        (652, 'Nantucket - Kiwi Berry Cktl.', 'morbi ut odio cras mi pede malesuada in imperdiet et commodo vulputate justo in blandit ultrices', 59.74, 98, '2020-09-07 00:00:00', 6, '-'),
                        (653, 'Wine - Ej Gallo Sierra Valley', 'nulla suspendisse potenti cras in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis', 28.12, 21, '2021-02-16 00:00:00', 5, '-'),
                        (654, 'Onions - Red Pearl', 'semper rutrum nulla nunc purus phasellus in felis donec semper sapien', 2.23, 93, '2021-05-01 00:00:00', 5, '-'),
                        (655, 'Soy Protein', 'in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat id mauris vulputate elementum nullam', 94.42, 14, '2020-08-07 00:00:00', 4, '-'),
                        (656, 'Sauce - Marinara', 'enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur', 5.62, 14, '2020-11-06 00:00:00', 4, '-'),
                        (657, 'Salt - Sea', 'justo morbi ut odio cras mi pede malesuada in imperdiet', 25.91, 95, '2020-11-25 00:00:00', 3, '-'),
                        (658, 'Wine - Jafflin Bourgongone', 'erat curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget', 91.01, 21, '2020-10-09 00:00:00', 4, '-'),
                        (659, 'Hot Choc Vending', 'sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus at diam nam', 52.05, 76, '2020-09-06 00:00:00', 4, '-'),
                        (660, 'Amaretto', 'tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh quisque id', 96.34, 57, '2020-06-19 00:00:00', 4, '-'),
                        (661, 'Garlic - Primerba, Paste', 'pede justo eu massa donec dapibus duis at velit eu est congue elementum in hac habitasse platea dictumst morbi', 16.36, 31, '2020-09-19 00:00:00', 4, '-'),
                        (662, 'Ecolab Silver Fusion', 'eu interdum eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat nulla', 88.79, 83, '2020-08-01 00:00:00', 3, '-'),
                        (663, 'Raisin - Golden', 'nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam', 58.76, 97, '2020-08-25 00:00:00', 5, '-'),
                        (664, 'Lettuce - Sea / Sea Asparagus', 'orci luctus et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis consequat dui nec', 41.73, 8, '2020-09-12 00:00:00', 5, '-'),
                        (665, 'Wine - Red, Gamay Noir', 'tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat', 6.72, 23, '2020-06-18 00:00:00', 3, '-'),
                        (666, 'Coffee - Decafenated', 'sed vel enim sit amet nunc viverra dapibus nulla suscipit ligula', 21.93, 74, '2020-07-09 00:00:00', 5, '-'),
                        (667, 'Mix - Cocktail Strawberry Daiquiri', 'pellentesque eget nunc donec quis orci eget orci vehicula condimentum curabitur in libero ut massa volutpat convallis', 52.74, 53, '2021-06-08 00:00:00', 6, '-'),
                        (668, 'Carbonated Water - Strawberry', 'cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel augue vestibulum rutrum rutrum neque', 40.86, 44, '2021-05-27 00:00:00', 3, '-'),
                        (669, 'Pepper - Red Bell', 'turpis donec posuere metus vitae ipsum aliquam non mauris morbi non lectus aliquam sit amet', 25.64, 41, '2020-07-12 00:00:00', 6, '-'),
                        (670, 'Ham - Black Forest', 'et eros vestibulum ac est lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut', 87.40, 56, '2021-05-19 00:00:00', 3, '-'),
                        (671, 'Cakes Assorted', 'et tempus semper est quam pharetra magna ac consequat metus sapien ut nunc vestibulum ante ipsum primis', 31.81, 79, '2020-08-03 00:00:00', 5, '-'),
                        (672, 'Wine - Domaine Boyar Royal', 'congue etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam', 25.10, 31, '2021-05-23 00:00:00', 3, '-'),
                        (673, 'Cheese - Brie,danish', 'elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper', 91.06, 42, '2020-12-13 00:00:00', 6, '-'),
                        (674, 'Bread - Kimel Stick Poly', 'in congue etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus', 79.45, 60, '2021-02-09 00:00:00', 6, '-'),
                        (675, 'Tomato - Green', 'integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed magna at nunc commodo placerat', 38.98, 18, '2020-10-01 00:00:00', 4, '-'),
                        (676, 'Extract - Lemon', 'suspendisse potenti in eleifend quam a odio in hac habitasse', 78.16, 5, '2021-05-04 00:00:00', 6, '-'),
                        (677, 'Tea - Orange Pekoe', 'id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat', 13.80, 5, '2021-04-09 00:00:00', 6, '-'),
                        (678, 'Langers - Mango Nectar', 'mauris eget massa tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh quisque id justo sit amet', 75.50, 24, '2020-12-08 00:00:00', 6, '-'),
                        (679, 'Apple - Delicious, Red', 'primis in faucibus orci luctus et ultrices posuere cubilia curae duis faucibus accumsan odio curabitur convallis duis', 74.54, 58, '2020-06-20 00:00:00', 6, '-'),
                        (680, 'Cleaner - Bleach', 'duis at velit eu est congue elementum in hac habitasse platea dictumst morbi vestibulum velit id pretium iaculis diam', 59.18, 88, '2021-04-28 00:00:00', 5, '-'),
                        (681, 'Spinach - Packaged', 'tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus', 24.33, 13, '2021-06-06 00:00:00', 3, '-'),
                        (682, 'Bacardi Breezer - Strawberry', 'in hac habitasse platea dictumst maecenas ut massa quis augue luctus tincidunt nulla mollis molestie', 37.22, 97, '2021-05-29 00:00:00', 6, '-'),
                        (683, 'Sobe - Green Tea', 'dui luctus rutrum nulla tellus in sagittis dui vel nisl duis ac nibh fusce', 52.08, 13, '2020-08-29 00:00:00', 5, '-'),
                        (684, 'Butter - Salted, Micro', 'convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia', 14.83, 68, '2021-05-04 00:00:00', 6, '-'),
                        (685, 'Spic And Span All Purpose', 'et ultrices posuere cubilia curae mauris viverra diam vitae quam suspendisse potenti nullam porttitor', 5.57, 77, '2021-01-19 00:00:00', 5, '-'),
                        (686, 'Milkettes - 2%', 'vel augue vestibulum rutrum rutrum neque aenean auctor gravida sem praesent id massa id nisl', 11.77, 32, '2021-06-06 00:00:00', 6, '-'),
                        (687, 'Quail Eggs - Canned', 'donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non mi integer ac neque', 72.23, 82, '2020-12-07 00:00:00', 6, '-'),
                        (688, 'Soap - Pine Sol Floor Cleaner', 'quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices', 97.73, 0, '2021-04-12 00:00:00', 4, '-'),
                        (689, 'Pail - 15l White, With Handle', 'praesent lectus vestibulum quam sapien varius ut blandit non interdum in', 73.84, 49, '2020-08-17 00:00:00', 3, '-'),
                        (690, 'Flounder - Fresh', 'ligula nec sem duis aliquam convallis nunc proin at turpis a pede posuere nonummy integer non velit donec diam', 47.02, 23, '2020-11-28 00:00:00', 4, '-'),
                        (691, 'Vol Au Vents', 'congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a', 25.05, 52, '2020-06-11 00:00:00', 3, '-'),
                        (692, 'Tea - Honey Green Tea', 'nascetur ridiculus mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus', 9.78, 93, '2021-03-28 00:00:00', 3, '-'),
                        (693, 'Nectarines', 'velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat', 53.85, 11, '2021-05-23 00:00:00', 6, '-'),
                        (694, 'Bagels Poppyseed', 'id luctus nec molestie sed justo pellentesque viverra pede ac diam cras pellentesque volutpat dui maecenas tristique est et', 77.76, 52, '2020-07-28 00:00:00', 5, '-'),
                        (695, 'Table Cloth 53x69 White', 'habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla', 92.17, 67, '2021-01-03 00:00:00', 3, '-'),
                        (696, 'Wine - Balbach Riverside', 'purus phasellus in felis donec semper sapien a libero nam dui proin', 45.95, 47, '2020-10-24 00:00:00', 4, '-'),
                        (697, 'Bread Country Roll', 'nulla elit ac nulla sed vel enim sit amet nunc viverra dapibus nulla suscipit ligula', 48.85, 46, '2020-07-07 00:00:00', 3, '-'),
                        (698, 'Wine - Tio Pepe Sherry Fino', 'odio curabitur convallis duis consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam', 58.48, 75, '2020-11-02 00:00:00', 5, '-'),
                        (699, 'Curry Paste - Madras', 'nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed', 50.49, 14, '2020-07-15 00:00:00', 6, '-'),
                        (700, 'Lime Cordial - Roses', 'ligula in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit', 4.09, 98, '2020-07-20 00:00:00', 5, '-'),
                        (701, 'Fish - Halibut, Cold Smoked', 'congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed', 4.66, 44, '2020-11-18 00:00:00', 4, '-'),
                        (702, 'Veal - Ground', 'ut nunc vestibulum ante ipsum primis in faucibus orci luctus et', 61.72, 36, '2020-09-10 00:00:00', 5, '-'),
                        (703, 'Marsala - Sperone, Fine, D.o.c.', 'viverra diam vitae quam suspendisse potenti nullam porttitor lacus at turpis donec posuere metus vitae', 75.52, 94, '2020-11-26 00:00:00', 3, '-'),
                        (704, 'Tabasco Sauce, 2 Oz', 'praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget', 47.85, 76, '2020-12-17 00:00:00', 3, '-'),
                        (705, 'Uniform Linen Charge', 'rhoncus sed vestibulum sit amet cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue', 53.02, 4, '2020-09-14 00:00:00', 5, '-'),
                        (706, 'Soup - Campbells Beef Noodle', 'pellentesque ultrices mattis odio donec vitae nisi nam ultrices libero non mattis pulvinar nulla', 28.68, 41, '2020-08-26 00:00:00', 4, '-'),
                        (707, 'Salmon - Atlantic, No Skin', 'metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean', 23.02, 44, '2020-11-26 00:00:00', 3, '-'),
                        (708, 'Rice - Jasmine Sented', 'dictumst maecenas ut massa quis augue luctus tincidunt nulla mollis molestie lorem quisque ut erat curabitur gravida nisi at nibh', 5.20, 58, '2020-09-15 00:00:00', 6, '-'),
                        (709, 'Wine La Vielle Ferme Cote Du', 'rhoncus mauris enim leo rhoncus sed vestibulum sit amet cursus id turpis integer aliquet massa', 23.11, 28, '2020-11-02 00:00:00', 6, '-'),
                        (710, 'Juice - Apple, 341 Ml', 'risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia sapien quis', 73.52, 35, '2020-07-18 00:00:00', 4, '-'),
                        (711, 'Lemon Balm - Fresh', 'pulvinar nulla pede ullamcorper augue a suscipit nulla elit ac nulla sed vel enim sit amet nunc viverra dapibus', 66.85, 68, '2020-09-04 00:00:00', 6, '-'),
                        (712, 'Garlic - Primerba, Paste', 'sed ante vivamus tortor duis mattis egestas metus aenean fermentum donec', 22.25, 89, '2020-07-08 00:00:00', 5, '-'),
                        (713, 'Chocolate - Milk, Callets', 'sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel', 15.33, 75, '2020-07-17 00:00:00', 6, '-'),
                        (714, 'Dill Weed - Dry', 'faucibus orci luctus et ultrices posuere cubilia curae mauris viverra diam vitae', 32.07, 72, '2021-01-26 00:00:00', 3, '-'),
                        (715, 'Beef - Montreal Smoked Brisket', 'elit proin interdum mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing', 68.72, 7, '2020-11-05 00:00:00', 5, '-'),
                        (716, 'Vaccum Bag - 14x20', 'erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus', 41.39, 17, '2021-04-13 00:00:00', 6, '-'),
                        (717, 'Soap - Mr.clean Floor Soap', 'lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum', 98.67, 4, '2020-07-29 00:00:00', 6, '-'),
                        (718, 'Sauce - Apple, Unsweetened', 'mauris vulputate elementum nullam varius nulla facilisi cras non velit', 35.30, 12, '2020-12-27 00:00:00', 4, '-'),
                        (719, 'Crush - Grape, 355 Ml', 'nulla sed vel enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac', 2.04, 49, '2020-12-14 00:00:00', 4, '-'),
                        (720, 'Cornstarch', 'vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum', 58.32, 4, '2020-08-26 00:00:00', 3, '-'),
                        (721, 'Dip - Tapenade', 'platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at', 81.86, 91, '2021-02-22 00:00:00', 6, '-'),
                        (722, 'Chicken - Livers', 'in ante vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae duis faucibus', 19.45, 44, '2021-03-26 00:00:00', 4, '-'),
                        (723, 'Wine - Casillero Deldiablo', 'quam pede lobortis ligula sit amet eleifend pede libero quis orci nullam molestie nibh in lectus', 30.36, 17, '2021-04-06 00:00:00', 4, '-'),
                        (724, 'Lambcasing', 'pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est risus auctor sed tristique in tempus sit amet', 55.42, 76, '2020-10-27 00:00:00', 6, '-'),
                        (725, 'Salmon Steak - Cohoe 8 Oz', 'sapien a libero nam dui proin leo odio porttitor id consequat in', 38.96, 21, '2020-09-10 00:00:00', 6, '-'),
                        (726, 'Cheese - Fontina', 'praesent blandit lacinia erat vestibulum sed magna at nunc commodo placerat praesent blandit nam nulla integer pede justo lacinia', 22.05, 85, '2021-03-25 00:00:00', 4, '-'),
                        (727, 'Pails With Lids', 'nulla tempus vivamus in felis eu sapien cursus vestibulum proin eu mi nulla ac enim in tempor turpis nec', 3.75, 52, '2020-10-04 00:00:00', 5, '-'),
                        (728, 'Pork - Smoked Kassler', 'duis bibendum morbi non quam nec dui luctus rutrum nulla tellus in sagittis dui vel nisl duis', 30.41, 4, '2021-01-18 00:00:00', 3, '-'),
                        (729, 'Juice - Cranberry, 341 Ml', 'in blandit ultrices enim lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non', 3.74, 48, '2020-12-19 00:00:00', 5, '-'),
                        (730, 'Lettuce - Red Leaf', 'sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel augue', 62.54, 39, '2021-02-25 00:00:00', 4, '-'),
                        (731, 'Garbag Bags - Black', 'convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh quisque id justo sit amet sapien dignissim vestibulum vestibulum', 10.00, 83, '2020-12-30 00:00:00', 3, '-'),
                        (732, 'Mustard - Individual Pkg', 'dui proin leo odio porttitor id consequat in consequat ut nulla sed', 39.85, 82, '2020-08-09 00:00:00', 6, '-'),
                        (733, 'Wine - White, Gewurtzraminer', 'sapien non mi integer ac neque duis bibendum morbi non quam', 20.81, 38, '2020-09-15 00:00:00', 4, '-'),
                        (734, 'Tea - Black Currant', 'sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel augue', 87.59, 82, '2021-03-25 00:00:00', 5, '-'),
                        (735, 'Chicken - Whole Fryers', 'eros vestibulum ac est lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut', 92.72, 44, '2020-08-23 00:00:00', 6, '-'),
                        (736, 'Iced Tea - Lemon, 460 Ml', 'cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel augue vestibulum', 10.87, 93, '2020-11-11 00:00:00', 6, '-'),
                        (737, 'Anchovy Paste - 56 G Tube', 'lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec molestie sed', 91.27, 73, '2021-03-02 00:00:00', 6, '-'),
                        (738, 'Spice - Chili Powder Mexican', 'nulla eget eros elementum pellentesque quisque porta volutpat erat quisque', 81.19, 46, '2021-01-15 00:00:00', 5, '-'),
                        (739, 'Milk - Buttermilk', 'ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu', 51.96, 46, '2020-07-09 00:00:00', 4, '-'),
                        (740, 'Teriyaki Sauce', 'in hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem', 74.90, 6, '2021-01-19 00:00:00', 6, '-'),
                        (741, 'Mcgillicuddy Vanilla Schnap', 'posuere felis sed lacus morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc rhoncus dui vel sem sed', 6.59, 8, '2021-04-25 00:00:00', 6, '-'),
                        (742, 'Syrup - Monin - Blue Curacao', 'elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus at velit vivamus vel nulla', 4.21, 0, '2020-10-24 00:00:00', 5, '-'),
                        (743, 'Bagels Poppyseed', 'praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante', 41.27, 46, '2020-07-05 00:00:00', 6, '-'),
                        (744, 'Bread - Focaccia Quarter', 'odio curabitur convallis duis consequat dui nec nisi volutpat eleifend donec ut', 97.63, 63, '2020-10-21 00:00:00', 5, '-'),
                        (745, 'Quinoa', 'consequat lectus in est risus auctor sed tristique in tempus sit amet sem fusce consequat nulla', 98.74, 75, '2020-06-20 00:00:00', 4, '-'),
                        (746, 'Eggplant - Regular', 'sed accumsan felis ut at dolor quis odio consequat varius integer ac leo', 17.56, 26, '2020-12-02 00:00:00', 6, '-'),
                        (747, 'Bagels Poppyseed', 'sit amet consectetuer adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante', 53.78, 22, '2020-08-26 00:00:00', 6, '-'),
                        (748, 'Bread - Hamburger Buns', 'ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae', 23.54, 93, '2020-09-13 00:00:00', 6, '-'),
                        (749, 'Bread - Roll, Calabrese', 'ante nulla justo aliquam quis turpis eget elit sodales scelerisque mauris sit amet eros', 85.75, 49, '2021-04-09 00:00:00', 5, '-'),
                        (750, 'Apricots - Dried', 'ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis', 38.67, 81, '2021-02-06 00:00:00', 3, '-'),
                        (751, 'Tea - Mint', 'hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat id mauris vulputate elementum nullam', 24.54, 17, '2020-12-27 00:00:00', 3, '-'),
                        (752, 'Beef - Shank', 'ut mauris eget massa tempor convallis nulla neque libero convallis eget eleifend luctus ultricies', 34.42, 24, '2021-04-20 00:00:00', 4, '-'),
                        (753, 'Soup - Beef, Base Mix', 'tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut', 42.17, 81, '2020-11-25 00:00:00', 4, '-'),
                        (754, 'Horseradish - Prepared', 'at velit eu est congue elementum in hac habitasse platea dictumst morbi vestibulum velit id', 58.71, 3, '2020-07-23 00:00:00', 5, '-'),
                        (755, 'Snapple Raspberry Tea', 'odio curabitur convallis duis consequat dui nec nisi volutpat eleifend donec ut', 53.58, 53, '2020-12-12 00:00:00', 5, '-'),
                        (756, 'Pastry - Apple Muffins - Mini', 'sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan felis', 39.85, 93, '2021-05-06 00:00:00', 3, '-'),
                        (757, 'Cheese - Cheddar, Old White', 'libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan felis', 89.36, 78, '2020-08-03 00:00:00', 6, '-'),
                        (758, 'Syrup - Monin - Granny Smith', 'id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus at velit', 8.14, 3, '2020-10-04 00:00:00', 5, '-'),
                        (759, 'Cinnamon Rolls', 'tortor duis mattis egestas metus aenean fermentum donec ut mauris', 62.92, 78, '2021-02-19 00:00:00', 4, '-'),
                        (760, 'Sparkling Wine - Rose, Freixenet', 'mauris eget massa tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh quisque id justo sit amet', 67.78, 32, '2020-06-25 00:00:00', 5, '-'),
                        (761, 'Sultanas', 'erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit', 7.33, 1, '2020-10-26 00:00:00', 6, '-'),
                        (762, 'Pepper - Green', 'in eleifend quam a odio in hac habitasse platea dictumst maecenas ut massa quis augue luctus', 97.54, 5, '2021-04-24 00:00:00', 3, '-'),
                        (763, 'Cheese - Ricotta', 'eros vestibulum ac est lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet', 25.22, 35, '2021-01-27 00:00:00', 4, '-'),
                        (764, 'Hot Choc Vending', 'et eros vestibulum ac est lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium', 82.25, 74, '2021-06-01 00:00:00', 6, '-'),
                        (765, 'Tomato - Tricolor Cherry', 'eu interdum eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus vivamus', 21.61, 34, '2020-11-17 00:00:00', 3, '-'),
                        (766, 'Cookie Double Choco', 'leo rhoncus sed vestibulum sit amet cursus id turpis integer aliquet massa', 72.75, 90, '2021-05-26 00:00:00', 4, '-'),
                        (767, 'Frangelico', 'orci nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate luctus', 59.70, 81, '2021-05-18 00:00:00', 4, '-'),
                        (768, 'Wine - Muscadet Sur Lie', 'turpis adipiscing lorem vitae mattis nibh ligula nec sem duis aliquam', 22.25, 89, '2020-07-21 00:00:00', 5, '-'),
                        (769, 'Steel Wool', 'mauris eget massa tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh', 20.32, 55, '2021-01-27 00:00:00', 5, '-'),
                        (770, 'Olives - Morracan Dired', 'consequat dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam', 32.72, 10, '2021-02-28 00:00:00', 4, '-'),
                        (771, 'Tomato Puree', 'adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in', 55.37, 37, '2020-10-27 00:00:00', 3, '-'),
                        (772, 'Sobe - Orange Carrot', 'sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at', 84.76, 80, '2021-01-08 00:00:00', 5, '-'),
                        (773, 'Beef Wellington', 'amet lobortis sapien sapien non mi integer ac neque duis bibendum morbi non quam nec', 20.72, 18, '2020-08-09 00:00:00', 4, '-'),
                        (774, 'Table Cloth 90x90 Colour', 'placerat praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget', 70.40, 12, '2021-01-13 00:00:00', 3, '-'),
                        (775, 'Flour - Semolina', 'fusce consequat nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis enim blandit mi in porttitor pede', 40.01, 63, '2020-12-07 00:00:00', 6, '-'),
                        (776, 'Sobe - Berry Energy', 'consequat dui nec nisi volutpat eleifend donec ut dolor morbi', 14.85, 70, '2021-01-10 00:00:00', 4, '-'),
                        (777, 'Mcguinness - Blue Curacao', 'ultrices enim lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque', 94.68, 60, '2020-06-13 00:00:00', 4, '-'),
                        (778, 'Bag Stand', 'nisi at nibh in hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer', 63.02, 22, '2021-01-18 00:00:00', 4, '-'),
                        (779, 'Waffle Stix', 'vel pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est risus auctor', 88.15, 18, '2020-12-13 00:00:00', 3, '-'),
                        (780, 'Bread - Frozen Basket Variety', 'nec molestie sed justo pellentesque viverra pede ac diam cras pellentesque volutpat dui maecenas tristique est et', 89.47, 2, '2020-12-25 00:00:00', 6, '-'),
                        (781, 'Wine - Shiraz South Eastern', 'sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean lectus pellentesque', 62.23, 47, '2021-01-16 00:00:00', 6, '-'),
                        (782, 'Wine - Jaboulet Cotes Du Rhone', 'eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque at', 84.37, 43, '2021-06-07 00:00:00', 5, '-'),
                        (783, 'Bandage - Finger Cots', 'ultrices enim lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque ultrices', 28.05, 64, '2021-03-20 00:00:00', 4, '-'),
                        (784, 'Bread Ww Cluster', 'nulla elit ac nulla sed vel enim sit amet nunc viverra dapibus', 24.96, 71, '2020-11-28 00:00:00', 5, '-'),
                        (785, 'Sauce - Plum', 'adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante ipsum primis', 4.87, 26, '2020-10-15 00:00:00', 5, '-'),
                        (786, 'Salmon - Atlantic, Skin On', 'quisque porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in', 40.60, 57, '2020-11-03 00:00:00', 4, '-'),
                        (787, 'Tea - Decaf Lipton', 'in hac habitasse platea dictumst maecenas ut massa quis augue luctus tincidunt nulla mollis molestie lorem', 99.45, 87, '2020-11-30 00:00:00', 5, '-'),
                        (788, 'Cake - Cake Sheet Macaroon', 'lobortis ligula sit amet eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque', 25.66, 63, '2021-05-25 00:00:00', 6, '-'),
                        (789, 'Wine - Magnotta, Merlot Sr Vqa', 'mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel augue', 95.54, 61, '2021-04-21 00:00:00', 4, '-'),
                        (790, 'Apples - Spartan', 'in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio', 40.39, 47, '2020-09-02 00:00:00', 6, '-'),
                        (791, 'Pie Box - Cello Window 2.5', 'donec vitae nisi nam ultrices libero non mattis pulvinar nulla pede ullamcorper augue a suscipit nulla elit ac', 84.34, 68, '2020-09-12 00:00:00', 3, '-'),
                        (792, 'Spice - Peppercorn Melange', 'at turpis a pede posuere nonummy integer non velit donec', 63.42, 53, '2021-04-23 00:00:00', 6, '-'),
                        (793, 'Cherries - Bing, Canned', 'nunc commodo placerat praesent blandit nam nulla integer pede justo lacinia eget tincidunt eget', 7.50, 74, '2021-05-20 00:00:00', 6, '-'),
                        (794, 'Bread - English Muffin', 'platea dictumst maecenas ut massa quis augue luctus tincidunt nulla mollis', 20.67, 70, '2020-09-26 00:00:00', 6, '-'),
                        (795, 'Trueblue - Blueberry', 'cubilia curae mauris viverra diam vitae quam suspendisse potenti nullam porttitor', 93.86, 81, '2021-04-24 00:00:00', 3, '-'),
                        (796, 'Longos - Penne With Pesto', 'turpis integer aliquet massa id lobortis convallis tortor risus dapibus', 95.72, 53, '2020-10-24 00:00:00', 5, '-'),
                        (797, 'Lamb - Loin, Trimmed, Boneless', 'eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a', 38.98, 97, '2020-09-04 00:00:00', 6, '-'),
                        (798, 'Wine - Rioja Campo Viejo', 'nulla ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi', 95.76, 84, '2021-02-17 00:00:00', 3, '-'),
                        (799, 'Loquat', 'eu est congue elementum in hac habitasse platea dictumst morbi vestibulum velit id pretium', 26.98, 66, '2020-09-15 00:00:00', 3, '-'),
                        (800, 'Hold Up Tool Storage Rack', 'nulla nisl nunc nisl duis bibendum felis sed interdum venenatis turpis enim blandit mi in', 4.35, 89, '2020-10-28 00:00:00', 3, '-'),
                        (801, 'Parsley - Dried', 'morbi odio odio elementum eu interdum eu tincidunt in leo maecenas pulvinar', 4.62, 61, '2020-07-25 00:00:00', 4, '-'),
                        (802, 'Plasticforkblack', 'nullam orci pede venenatis non sodales sed tincidunt eu felis fusce posuere felis sed', 50.81, 58, '2020-12-23 00:00:00', 6, '-'),
                        (803, 'Potato - Sweet', 'a odio in hac habitasse platea dictumst maecenas ut massa quis augue luctus tincidunt nulla', 63.85, 59, '2020-12-09 00:00:00', 4, '-'),
                        (804, 'Coffee - Cafe Moreno', 'ut massa volutpat convallis morbi odio odio elementum eu interdum eu tincidunt in leo', 15.59, 91, '2021-01-02 00:00:00', 6, '-'),
                        (805, 'Wine - Red, Colio Cabernet', 'lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium', 96.99, 59, '2021-03-23 00:00:00', 3, '-'),
                        (806, 'Ostrich - Fan Fillet', 'orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel est donec odio', 60.59, 23, '2020-11-23 00:00:00', 4, '-'),
                        (807, 'Green Tea Refresher', 'sed accumsan felis ut at dolor quis odio consequat varius integer ac leo pellentesque ultrices mattis odio donec vitae', 57.25, 90, '2021-05-04 00:00:00', 3, '-'),
                        (808, 'Flour - Rye', 'lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est risus auctor', 88.01, 18, '2021-02-03 00:00:00', 6, '-'),
                        (809, 'Sugar Thermometer', 'eu orci mauris lacinia sapien quis libero nullam sit amet', 97.85, 81, '2020-09-11 00:00:00', 6, '-'),
                        (810, 'Wine - Tio Pepe Sherry Fino', 'molestie hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc donec quis orci eget', 47.11, 67, '2021-02-20 00:00:00', 3, '-'),
                        (811, 'Cassis', 'ultrices posuere cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin ut suscipit a feugiat et', 94.98, 96, '2021-01-17 00:00:00', 3, '-'),
                        (812, 'Ice Cream - Super Sandwich', 'tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh quisque id justo sit amet sapien', 15.08, 84, '2021-01-19 00:00:00', 6, '-'),
                        (813, 'Sauce - Salsa', 'lobortis ligula sit amet eleifend pede libero quis orci nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras', 88.19, 73, '2021-05-26 00:00:00', 3, '-'),
                        (814, 'Jerusalem Artichoke', 'faucibus cursus urna ut tellus nulla ut erat id mauris vulputate', 60.16, 87, '2021-03-05 00:00:00', 3, '-'),
                        (815, 'Juice - Prune', 'luctus ultricies eu nibh quisque id justo sit amet sapien dignissim vestibulum vestibulum ante ipsum primis in faucibus', 70.29, 45, '2020-06-22 00:00:00', 6, '-'),
                        (816, 'Lamb - Sausage Casings', 'justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec', 52.51, 89, '2020-09-05 00:00:00', 5, '-'),
                        (817, 'Cleaner - Lime Away', 'nulla integer pede justo lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem id ligula suspendisse', 24.67, 39, '2021-02-14 00:00:00', 4, '-'),
                        (818, 'Flour Dark Rye', 'ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim leo rhoncus sed', 99.45, 93, '2020-08-20 00:00:00', 4, '-'),
                        (819, 'Chef Hat 20cm', 'justo sit amet sapien dignissim vestibulum vestibulum ante ipsum primis in faucibus', 53.60, 55, '2021-01-16 00:00:00', 3, '-'),
                        (820, 'Pork - Sausage, Medium', 'in congue etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus', 56.86, 26, '2021-02-25 00:00:00', 4, '-'),
                        (821, 'Iced Tea - Lemon, 460 Ml', 'tortor risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia', 3.29, 68, '2021-03-20 00:00:00', 5, '-'),
                        (822, 'Lobak', 'dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia', 82.45, 27, '2021-01-28 00:00:00', 5, '-'),
                        (823, 'Juice - Apple, 500 Ml', 'ut suscipit a feugiat et eros vestibulum ac est lacinia nisi venenatis tristique fusce', 47.96, 50, '2021-04-02 00:00:00', 3, '-'),
                        (824, 'Cheese - La Sauvagine', 'amet sapien dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus', 76.15, 61, '2021-01-17 00:00:00', 4, '-'),
                        (825, 'Plasticknivesblack', 'nibh in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio', 46.41, 62, '2020-07-28 00:00:00', 5, '-'),
                        (826, 'Broom - Push', 'morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec molestie sed justo pellentesque viverra', 65.92, 65, '2020-10-29 00:00:00', 3, '-'),
                        (827, 'Cookies - Assorted', 'diam in magna bibendum imperdiet nullam orci pede venenatis non sodales sed tincidunt eu felis fusce posuere felis sed lacus', 2.58, 66, '2020-06-30 00:00:00', 6, '-'),
                        (828, 'Shrimp - 150 - 250', 'sit amet cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus', 72.34, 29, '2021-04-27 00:00:00', 5, '-'),
                        (829, 'Toamtoes 6x7 Select', 'est lacinia nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu', 74.25, 44, '2020-11-05 00:00:00', 6, '-'),
                        (830, 'Duck - Breast', 'consequat ut nulla sed accumsan felis ut at dolor quis odio', 93.37, 100, '2020-10-04 00:00:00', 5, '-'),
                        (831, 'Spice - Chili Powder Mexican', 'sapien a libero nam dui proin leo odio porttitor id', 7.24, 68, '2020-07-25 00:00:00', 3, '-'),
                        (832, 'Mushroom - Chanterelle Frozen', 'justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut', 9.80, 27, '2020-10-01 00:00:00', 5, '-'),
                        (833, 'Wine - Red, Gallo, Merlot', 'pede libero quis orci nullam molestie nibh in lectus pellentesque at nulla suspendisse potenti cras in purus', 49.76, 31, '2021-05-31 00:00:00', 6, '-'),
                        (834, 'Wine - Puligny Montrachet A.', 'nulla ut erat id mauris vulputate elementum nullam varius nulla', 88.48, 10, '2020-11-18 00:00:00', 3, '-'),
                        (835, 'Sole - Dover, Whole, Fresh', 'in faucibus orci luctus et ultrices posuere cubilia curae mauris viverra diam vitae quam suspendisse potenti', 54.55, 42, '2020-07-22 00:00:00', 5, '-'),
                        (836, 'Pork Ham Prager', 'adipiscing elit proin risus praesent lectus vestibulum quam sapien varius ut blandit', 35.20, 15, '2021-02-16 00:00:00', 6, '-'),
                        (837, 'Beef - Sushi Flat Iron Steak', 'pellentesque volutpat dui maecenas tristique est et tempus semper est quam pharetra magna ac consequat metus sapien ut nunc', 24.61, 9, '2020-12-17 00:00:00', 6, '-'),
                        (838, 'General Purpose Trigger', 'lacus morbi quis tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus', 57.76, 89, '2020-07-24 00:00:00', 4, '-'),
                        (839, 'Chicken - White Meat With Tender', 'tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum donec', 43.96, 64, '2020-11-13 00:00:00', 6, '-'),
                        (840, 'Veal - Osso Bucco', 'tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat', 47.20, 48, '2020-11-23 00:00:00', 4, '-'),
                        (841, 'Soup - Beef Conomme, Dry', 'lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed magna at nunc commodo placerat praesent blandit nam', 81.56, 86, '2020-07-17 00:00:00', 5, '-'),
                        (842, 'Aromat Spice / Seasoning', 'nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus', 53.24, 43, '2021-01-16 00:00:00', 5, '-'),
                        (843, 'Veal - Loin', 'fringilla rhoncus mauris enim leo rhoncus sed vestibulum sit amet cursus id turpis', 15.52, 66, '2021-04-07 00:00:00', 3, '-'),
                        (844, 'Beef - Cooked, Corned', 'dictumst aliquam augue quam sollicitudin vitae consectetuer eget rutrum at lorem integer tincidunt', 62.21, 56, '2021-04-29 00:00:00', 5, '-'),
                        (845, 'Crawfish', 'malesuada in imperdiet et commodo vulputate justo in blandit ultrices enim lorem ipsum dolor sit amet', 8.68, 26, '2020-09-06 00:00:00', 6, '-'),
                        (846, 'Pastry - Mini French Pastries', 'amet cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi', 30.74, 66, '2021-01-12 00:00:00', 3, '-'),
                        (847, 'Food Colouring - Green', 'quis turpis eget elit sodales scelerisque mauris sit amet eros suspendisse', 64.27, 12, '2020-12-22 00:00:00', 3, '-'),
                        (848, 'Chicken - Breast, 5 - 7 Oz', 'vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci luctus et ultrices', 32.82, 72, '2021-03-25 00:00:00', 6, '-'),
                        (849, 'Brownies - Two Bite, Chocolate', 'ultrices libero non mattis pulvinar nulla pede ullamcorper augue a', 69.04, 69, '2021-05-03 00:00:00', 6, '-'),
                        (850, 'Peppercorns - Green', 'vitae ipsum aliquam non mauris morbi non lectus aliquam sit amet diam in magna bibendum imperdiet', 59.43, 11, '2020-07-11 00:00:00', 6, '-'),
                        (851, 'Beef Dry Aged Tenderloin Aaa', 'morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl nunc rhoncus dui', 55.63, 31, '2020-11-26 00:00:00', 5, '-'),
                        (852, 'Soup - Cream Of Potato / Leek', 'ut nulla sed accumsan felis ut at dolor quis odio consequat varius integer ac leo', 4.49, 52, '2020-10-27 00:00:00', 4, '-'),
                        (853, 'Corn - On The Cob', 'ipsum ac tellus semper interdum mauris ullamcorper purus sit amet nulla quisque', 98.90, 51, '2020-09-02 00:00:00', 4, '-'),
                        (854, 'Cream - 18%', 'integer pede justo lacinia eget tincidunt eget tempus vel pede morbi porttitor', 37.33, 74, '2021-05-03 00:00:00', 5, '-'),
                        (855, 'Lobster - Cooked', 'interdum in ante vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia', 9.93, 91, '2021-04-03 00:00:00', 6, '-'),
                        (856, 'Pork - Hock And Feet Attached', 'ultrices enim lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque ultrices phasellus id', 47.68, 26, '2021-06-07 00:00:00', 3, '-'),
                        (857, 'Wine - Red, Marechal Foch', 'phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in', 78.94, 77, '2021-04-02 00:00:00', 3, '-'),
                        (858, 'Salmon Steak - Cohoe 8 Oz', 'aliquet at feugiat non pretium quis lectus suspendisse potenti in eleifend quam a', 3.38, 98, '2021-05-23 00:00:00', 6, '-'),
                        (859, 'Salmon Steak - Cohoe 8 Oz', 'mi in porttitor pede justo eu massa donec dapibus duis at', 61.72, 11, '2021-03-24 00:00:00', 4, '-'),
                        (860, 'Onions - Vidalia', 'maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas', 7.96, 24, '2020-07-21 00:00:00', 6, '-'),
                        (861, 'Cheese - Brick With Onion', 'eleifend quam a odio in hac habitasse platea dictumst maecenas ut massa quis', 83.98, 12, '2020-08-29 00:00:00', 3, '-'),
                        (862, 'Juice - Apple, 500 Ml', 'ligula in lacus curabitur at ipsum ac tellus semper interdum', 91.83, 41, '2020-06-20 00:00:00', 6, '-'),
                        (863, 'Coffee Cup 12oz 5342cd', 'mauris ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus at diam nam tristique', 91.88, 60, '2021-04-28 00:00:00', 6, '-'),
                        (864, 'Appetizer - Crab And Brie', 'metus sapien ut nunc vestibulum ante ipsum primis in faucibus orci luctus et ultrices', 77.29, 94, '2021-04-30 00:00:00', 5, '-'),
                        (865, 'Heavy Duty Dust Pan', 'ligula nec sem duis aliquam convallis nunc proin at turpis a pede posuere nonummy integer non velit donec', 97.70, 6, '2020-07-25 00:00:00', 6, '-'),
                        (866, 'Devonshire Cream', 'mattis egestas metus aenean fermentum donec ut mauris eget massa tempor convallis', 28.21, 6, '2021-01-04 00:00:00', 4, '-'),
                        (867, 'Soup - Chicken And Wild Rice', 'urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo etiam pretium iaculis justo', 36.20, 74, '2020-07-29 00:00:00', 5, '-'),
                        (868, 'Lamb - Ground', 'nulla sed vel enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at', 67.34, 34, '2021-05-09 00:00:00', 5, '-'),
                        (869, 'Nut - Walnut, Pieces', 'praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante vestibulum ante', 90.88, 63, '2021-02-24 00:00:00', 4, '-'),
                        (870, 'Pail With Metal Handle 16l White', 'diam cras pellentesque volutpat dui maecenas tristique est et tempus semper', 67.41, 96, '2020-10-12 00:00:00', 4, '-'),
                        (871, 'Cheese - Stilton', 'porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis', 54.74, 84, '2021-05-24 00:00:00', 3, '-'),
                        (872, 'Edible Flower - Mixed', 'massa quis augue luctus tincidunt nulla mollis molestie lorem quisque ut erat', 17.58, 50, '2020-12-08 00:00:00', 3, '-'),
                        (873, 'Vinegar - Rice', 'volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim leo rhoncus', 13.34, 60, '2021-01-25 00:00:00', 4, '-'),
                        (874, 'Jameson - Irish Whiskey', 'ipsum integer a nibh in quis justo maecenas rhoncus aliquam lacus morbi quis tortor', 70.75, 42, '2021-04-23 00:00:00', 4, '-'),
                        (875, 'Milk - Condensed', 'nec sem duis aliquam convallis nunc proin at turpis a pede posuere nonummy', 72.56, 57, '2020-06-30 00:00:00', 3, '-'),
                        (876, 'Coffee - Beans, Whole', 'cras in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient', 38.07, 31, '2021-05-06 00:00:00', 5, '-'),
                        (877, 'Tea - Honey Green Tea', 'hac habitasse platea dictumst aliquam augue quam sollicitudin vitae consectetuer eget', 34.94, 59, '2020-07-15 00:00:00', 4, '-'),
                        (878, 'Mountain Dew', 'sollicitudin ut suscipit a feugiat et eros vestibulum ac est lacinia nisi venenatis tristique fusce', 72.29, 78, '2020-06-18 00:00:00', 3, '-'),
                        (879, 'Dehydrated Kelp Kombo', 'posuere felis sed lacus morbi sem mauris laoreet ut rhoncus aliquet pulvinar sed nisl', 19.22, 42, '2020-11-24 00:00:00', 4, '-'),
                        (880, 'Ham - Cooked Italian', 'porttitor lacus at turpis donec posuere metus vitae ipsum aliquam non mauris morbi non lectus aliquam', 69.17, 36, '2020-09-03 00:00:00', 4, '-'),
                        (881, 'Pasta - Penne, Rigate, Dry', 'sed vel enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper', 68.17, 14, '2020-07-24 00:00:00', 3, '-'),
                        (882, 'Vinegar - White Wine', 'ultrices aliquet maecenas leo odio condimentum id luctus nec molestie sed justo pellentesque viverra pede ac diam', 1.41, 95, '2021-01-02 00:00:00', 4, '-'),
                        (883, 'Chicken - Leg / Back Attach', 'sed augue aliquam erat volutpat in congue etiam justo etiam pretium', 62.32, 8, '2020-12-06 00:00:00', 3, '-'),
                        (884, 'Dc Hikiage Hira Huba', 'duis bibendum felis sed interdum venenatis turpis enim blandit mi in porttitor pede justo eu massa donec dapibus duis', 86.10, 88, '2020-12-31 00:00:00', 3, '-'),
                        (885, 'Beets', 'morbi odio odio elementum eu interdum eu tincidunt in leo maecenas pulvinar lobortis est', 4.77, 79, '2020-09-19 00:00:00', 5, '-'),
                        (886, 'Cinnamon Buns Sticky', 'neque sapien placerat ante nulla justo aliquam quis turpis eget elit sodales scelerisque mauris sit amet eros suspendisse accumsan', 84.08, 81, '2020-09-06 00:00:00', 4, '-'),
                        (887, 'Bagels Poppyseed', 'massa id nisl venenatis lacinia aenean sit amet justo morbi ut odio cras mi pede malesuada in imperdiet et commodo', 24.20, 32, '2021-03-19 00:00:00', 6, '-'),
                        (888, 'Pork - Loin, Boneless', 'aliquet pulvinar sed nisl nunc rhoncus dui vel sem sed sagittis nam', 30.54, 31, '2021-01-31 00:00:00', 3, '-'),
                        (889, 'Broom And Broom Rack White', 'aenean fermentum donec ut mauris eget massa tempor convallis nulla neque libero convallis eget eleifend luctus ultricies eu nibh quisque', 65.63, 63, '2020-07-16 00:00:00', 5, '-'),
                        (890, 'Filo Dough', 'amet cursus id turpis integer aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan', 29.75, 8, '2021-01-31 00:00:00', 4, '-'),
                        (891, 'Mushroom - Morels, Dry', 'tellus nulla ut erat id mauris vulputate elementum nullam varius', 93.01, 99, '2021-05-05 00:00:00', 5, '-'),
                        (892, 'Milkettes - 2%', 'ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt', 39.56, 27, '2021-01-25 00:00:00', 6, '-'),
                        (893, 'Flour - Buckwheat, Dark', 'pellentesque at nulla suspendisse potenti cras in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient', 63.49, 73, '2021-02-23 00:00:00', 5, '-'),
                        (894, 'Lemonade - Island Tea, 591 Ml', 'massa id lobortis convallis tortor risus dapibus augue vel accumsan', 87.53, 17, '2020-07-29 00:00:00', 5, '-'),
                        (895, 'Cup - 8oz Coffee Perforated', 'integer non velit donec diam neque vestibulum eget vulputate ut ultrices vel augue vestibulum', 4.99, 51, '2021-03-24 00:00:00', 5, '-'),
                        (896, 'Wine - Periguita Fonseca', 'in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla', 28.30, 60, '2021-01-09 00:00:00', 5, '-'),
                        (897, 'Sour Puss - Tangerine', 'nisi venenatis tristique fusce congue diam id ornare imperdiet sapien urna pretium nisl ut volutpat sapien arcu sed augue', 2.28, 23, '2021-03-14 00:00:00', 4, '-'),
                        (898, 'Pie Shells 10', 'dui nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus mauris enim leo rhoncus sed', 93.69, 5, '2020-07-03 00:00:00', 4, '-'),
                        (899, 'Steampan Lid', 'accumsan odio curabitur convallis duis consequat dui nec nisi volutpat eleifend donec ut dolor morbi', 74.10, 70, '2020-09-23 00:00:00', 6, '-'),
                        (900, 'Flower - Leather Leaf Fern', 'elementum eu interdum eu tincidunt in leo maecenas pulvinar lobortis est', 74.87, 40, '2020-11-21 00:00:00', 4, '-'),
                        (901, 'Tea - Grapefruit Green Tea', 'mauris viverra diam vitae quam suspendisse potenti nullam porttitor lacus at turpis donec posuere metus vitae', 55.42, 40, '2021-03-10 00:00:00', 5, '-'),
                        (902, 'Nacho Chips', 'pharetra magna ac consequat metus sapien ut nunc vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia', 8.37, 22, '2020-12-20 00:00:00', 5, '-'),
                        (903, 'Apples - Spartan', 'dignissim vestibulum vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere', 45.92, 93, '2021-02-24 00:00:00', 3, '-'),
                        (904, 'Salami - Genova', 'mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate', 13.74, 97, '2020-07-16 00:00:00', 4, '-'),
                        (905, 'Absolut Citron', 'dapibus dolor vel est donec odio justo sollicitudin ut suscipit a feugiat et eros', 88.20, 32, '2020-10-23 00:00:00', 4, '-'),
                        (906, 'Lumpfish Black', 'tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed magna at nunc commodo', 56.77, 62, '2020-07-17 00:00:00', 5, '-'),
                        (907, 'Lamb - Whole, Frozen', 'duis aliquam convallis nunc proin at turpis a pede posuere nonummy integer non velit', 16.64, 39, '2020-11-10 00:00:00', 5, '-'),
                        (908, 'Soup - Campbells', 'sagittis dui vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non pretium quis', 58.28, 78, '2020-12-13 00:00:00', 4, '-'),
                        (909, 'Bread - Mini Hamburger Bun', 'eget tempus vel pede morbi porttitor lorem id ligula suspendisse ornare consequat lectus in est risus auctor sed tristique', 3.98, 56, '2021-05-10 00:00:00', 4, '-'),
                        (910, 'Beef - Top Butt Aaa', 'ut suscipit a feugiat et eros vestibulum ac est lacinia nisi', 70.60, 93, '2020-10-23 00:00:00', 5, '-'),
                        (911, 'The Pop Shoppe - Root Beer', 'vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam', 81.50, 97, '2020-11-28 00:00:00', 3, '-'),
                        (912, 'Wine - Niagara Peninsula Vqa', 'erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper', 77.05, 87, '2021-03-31 00:00:00', 6, '-'),
                        (913, 'Wine - Red, Mouton Cadet', 'nec sem duis aliquam convallis nunc proin at turpis a pede posuere nonummy', 16.96, 32, '2020-12-05 00:00:00', 5, '-'),
                        (914, 'Longos - Chicken Cordon Bleu', 'interdum eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat', 64.01, 90, '2020-06-21 00:00:00', 4, '-'),
                        (915, 'Lamb - Ground', 'metus aenean fermentum donec ut mauris eget massa tempor convallis nulla', 73.04, 92, '2020-11-07 00:00:00', 3, '-'),
                        (916, 'Sour Puss Sour Apple', 'nonummy maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros', 59.71, 1, '2021-05-21 00:00:00', 4, '-'),
                        (917, 'Gingerale - Diet - Schweppes', 'enim sit amet nunc viverra dapibus nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper', 80.01, 96, '2020-12-21 00:00:00', 4, '-'),
                        (918, 'Soup - Base Broth Chix', 'nulla suscipit ligula in lacus curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus', 1.82, 45, '2020-08-03 00:00:00', 4, '-'),
                        (919, 'Bread - French Stick', 'mauris viverra diam vitae quam suspendisse potenti nullam porttitor lacus at turpis donec posuere metus vitae', 62.49, 73, '2020-09-18 00:00:00', 4, '-'),
                        (920, 'Turnip - White, Organic', 'nisi vulputate nonummy maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta', 43.91, 63, '2021-05-30 00:00:00', 5, '-'),
                        (921, 'Flour - Semolina', 'accumsan felis ut at dolor quis odio consequat varius integer ac leo pellentesque ultrices mattis odio donec', 25.44, 16, '2020-12-17 00:00:00', 5, '-'),
                        (922, 'Snapple Lemon Tea', 'nec nisi volutpat eleifend donec ut dolor morbi vel lectus in quam fringilla rhoncus', 92.30, 49, '2020-12-06 00:00:00', 6, '-'),
                        (923, 'Chocolate - Semi Sweet', 'justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut', 93.91, 46, '2020-11-12 00:00:00', 3, '-'),
                        (924, 'Apple - Fuji', 'ut tellus nulla ut erat id mauris vulputate elementum nullam varius', 82.27, 22, '2020-12-08 00:00:00', 6, '-'),
                        (925, 'Oil - Grapeseed Oil', 'luctus et ultrices posuere cubilia curae duis faucibus accumsan odio', 11.68, 87, '2020-09-05 00:00:00', 5, '-'),
                        (926, 'Ham - Cooked', 'orci mauris lacinia sapien quis libero nullam sit amet turpis elementum ligula vehicula consequat morbi a ipsum', 57.01, 16, '2021-02-10 00:00:00', 4, '-'),
                        (927, 'Blackberries', 'aenean lectus pellentesque eget nunc donec quis orci eget orci vehicula condimentum curabitur in libero ut massa volutpat convallis morbi', 22.24, 17, '2020-07-21 00:00:00', 4, '-'),
                        (928, 'Onions - Spanish', 'tortor duis mattis egestas metus aenean fermentum donec ut mauris eget massa tempor convallis nulla neque', 99.83, 15, '2021-06-09 00:00:00', 3, '-'),
                        (929, 'Wheat - Soft Kernal Of Wheat', 'non velit donec diam neque vestibulum eget vulputate ut ultrices vel', 38.36, 28, '2020-08-18 00:00:00', 5, '-'),
                        (930, 'Tandoori Curry Paste', 'sed tristique in tempus sit amet sem fusce consequat nulla nisl nunc nisl duis bibendum', 15.51, 7, '2021-04-03 00:00:00', 4, '-'),
                        (931, 'Ice Cream Bar - Oreo Sandwich', 'eget vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus', 29.51, 43, '2020-09-09 00:00:00', 4, '-'),
                        (932, 'Instant Coffee', 'adipiscing elit proin interdum mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus', 67.65, 26, '2021-03-16 00:00:00', 4, '-'),
                        (933, 'Yogurt - Blueberry, 175 Gr', 'tincidunt eu felis fusce posuere felis sed lacus morbi sem mauris laoreet ut rhoncus aliquet', 93.57, 8, '2020-09-07 00:00:00', 5, '-'),
                        (934, 'Juice - Orange 1.89l', 'habitasse platea dictumst morbi vestibulum velit id pretium iaculis diam erat fermentum justo nec condimentum neque sapien placerat ante nulla', 24.33, 63, '2020-07-20 00:00:00', 4, '-'),
                        (935, 'Clams - Littleneck, Whole', 'ut dolor morbi vel lectus in quam fringilla rhoncus mauris', 80.37, 45, '2020-08-19 00:00:00', 4, '-'),
                        (936, 'Chicken - Whole Fryers', 'ut rhoncus aliquet pulvinar sed nisl nunc rhoncus dui vel sem sed sagittis nam congue risus semper porta volutpat quam', 59.14, 59, '2021-01-09 00:00:00', 3, '-'),
                        (937, 'Tart - Lemon', 'sem fusce consequat nulla nisl nunc nisl duis bibendum felis', 56.34, 88, '2020-10-06 00:00:00', 6, '-'),
                        (938, 'Pesto - Primerba, Paste', 'lectus pellentesque eget nunc donec quis orci eget orci vehicula condimentum curabitur in libero ut massa volutpat', 85.67, 27, '2021-01-16 00:00:00', 6, '-'),
                        (939, 'Apple - Granny Smith', 'convallis nunc proin at turpis a pede posuere nonummy integer non', 77.92, 68, '2020-09-30 00:00:00', 4, '-'),
                        (940, 'Cranberries - Dry', 'pellentesque volutpat dui maecenas tristique est et tempus semper est', 50.45, 87, '2020-08-14 00:00:00', 5, '-'),
                        (941, 'Sponge Cake Mix - Chocolate', 'eros suspendisse accumsan tortor quis turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum', 72.18, 84, '2021-03-04 00:00:00', 5, '-'),
                        (942, 'Daikon Radish', 'a ipsum integer a nibh in quis justo maecenas rhoncus aliquam lacus morbi quis', 12.90, 47, '2021-05-30 00:00:00', 6, '-'),
                        (943, 'Bread - Roll, Whole Wheat', 'orci luctus et ultrices posuere cubilia curae donec pharetra magna vestibulum', 85.47, 95, '2020-09-05 00:00:00', 6, '-'),
                        (944, 'Wine - White, French Cross', 'convallis nulla neque libero convallis eget eleifend luctus ultricies eu', 19.88, 88, '2021-01-06 00:00:00', 3, '-'),
                        (945, 'Numi - Assorted Teas', 'hendrerit at vulputate vitae nisl aenean lectus pellentesque eget nunc', 29.59, 7, '2020-12-22 00:00:00', 3, '-'),
                        (946, 'Longos - Chicken Cordon Bleu', 'vitae consectetuer eget rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed magna at nunc', 46.23, 46, '2021-05-26 00:00:00', 5, '-'),
                        (947, 'Spice - Pepper Portions', 'nunc proin at turpis a pede posuere nonummy integer non', 7.48, 100, '2020-08-29 00:00:00', 4, '-'),
                        (948, 'Pastry - Cheese Baked Scones', 'rutrum at lorem integer tincidunt ante vel ipsum praesent blandit lacinia erat vestibulum sed magna at nunc commodo placerat', 48.37, 3, '2020-08-19 00:00:00', 3, '-'),
                        (949, 'Sprouts - Pea', 'urna pretium nisl ut volutpat sapien arcu sed augue aliquam erat volutpat in congue etiam justo etiam pretium', 76.76, 82, '2021-02-02 00:00:00', 3, '-'),
                        (950, 'Yoghurt Tubes', 'sapien sapien non mi integer ac neque duis bibendum morbi non', 97.98, 34, '2020-10-01 00:00:00', 4, '-'),
                        (951, 'Ginger - Pickled', 'cras in purus eu magna vulputate luctus cum sociis natoque penatibus et magnis dis parturient', 49.31, 56, '2020-06-28 00:00:00', 4, '-'),
                        (952, 'Salmon Steak - Cohoe 6 Oz', 'vel accumsan tellus nisi eu orci mauris lacinia sapien quis libero nullam', 16.26, 35, '2020-06-18 00:00:00', 3, '-'),
                        (953, 'Loaf Pan - 2 Lb, Foil', 'in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices', 31.72, 85, '2020-08-29 00:00:00', 5, '-'),
                        (954, 'Pastry - Choclate Baked', 'at turpis a pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate ut ultrices vel augue', 64.81, 65, '2021-02-08 00:00:00', 3, '-'),
                        (955, 'Mustard - Seed', 'pede posuere nonummy integer non velit donec diam neque vestibulum eget vulputate ut ultrices', 21.70, 7, '2021-03-09 00:00:00', 4, '-'),
                        (956, 'Mushroom - Enoki, Fresh', 'curae duis faucibus accumsan odio curabitur convallis duis consequat dui nec nisi volutpat eleifend', 94.14, 36, '2021-06-03 00:00:00', 6, '-'),
                        (957, 'Coffee - Colombian, Portioned', 'enim in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis nibh', 30.80, 88, '2020-11-29 00:00:00', 4, '-'),
                        (958, 'Juice - Ocean Spray Cranberry', 'pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc', 33.25, 93, '2020-06-14 00:00:00', 6, '-'),
                        (959, 'Tomato Puree', 'quis turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum donec ut mauris', 87.22, 46, '2020-07-29 00:00:00', 4, '-'),
                        (960, 'Wine - Rosso Del Veronese Igt', 'elit proin risus praesent lectus vestibulum quam sapien varius ut blandit non interdum in ante', 78.05, 45, '2021-05-28 00:00:00', 3, '-'),
                        (961, 'Wine - Fume Blanc Fetzer', 'aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non mi integer ac', 1.16, 46, '2020-10-25 00:00:00', 4, '-'),
                        (962, 'Goldschalger', 'erat curabitur gravida nisi at nibh in hac habitasse platea dictumst aliquam', 37.26, 91, '2021-03-16 00:00:00', 4, '-'),
                        (963, 'Wine - Manischewitz Concord', 'id sapien in sapien iaculis congue vivamus metus arcu adipiscing', 48.87, 53, '2021-04-20 00:00:00', 4, '-'),
                        (964, 'Beets - Golden', 'integer a nibh in quis justo maecenas rhoncus aliquam lacus morbi quis tortor id nulla ultrices aliquet maecenas', 42.69, 72, '2020-09-11 00:00:00', 5, '-'),
                        (965, 'Oysters - Smoked', 'sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate vitae nisl aenean', 41.69, 0, '2021-04-29 00:00:00', 3, '-'),
                        (966, 'Salmon Atl.whole 8 - 10 Lb', 'dictumst maecenas ut massa quis augue luctus tincidunt nulla mollis molestie lorem quisque ut erat curabitur gravida', 30.31, 74, '2021-01-03 00:00:00', 6, '-'),
                        (967, 'Rolled Oats', 'quam a odio in hac habitasse platea dictumst maecenas ut massa quis augue', 30.25, 62, '2020-09-07 00:00:00', 4, '-'),
                        (968, 'Monkfish - Fresh', 'ultrices posuere cubilia curae donec pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non', 71.71, 98, '2020-10-16 00:00:00', 6, '-'),
                        (969, 'Carbonated Water - Blackcherry', 'aliquet massa id lobortis convallis tortor risus dapibus augue vel accumsan tellus nisi eu orci mauris lacinia sapien', 62.44, 94, '2021-04-21 00:00:00', 5, '-'),
                        (970, 'Pur Source', 'maecenas ut massa quis augue luctus tincidunt nulla mollis molestie lorem', 35.58, 28, '2020-08-21 00:00:00', 3, '-'),
                        (971, 'Pie Filling - Pumpkin', 'tortor id nulla ultrices aliquet maecenas leo odio condimentum id luctus nec molestie sed justo pellentesque', 1.38, 46, '2020-12-01 00:00:00', 5, '-'),
                        (972, 'Wonton Wrappers', 'primis in faucibus orci luctus et ultrices posuere cubilia curae donec pharetra magna', 61.63, 19, '2020-09-26 00:00:00', 3, '-'),
                        (973, 'Straw - Regular', 'luctus rutrum nulla tellus in sagittis dui vel nisl duis ac nibh fusce lacus purus aliquet at feugiat non', 14.67, 3, '2021-03-24 00:00:00', 4, '-'),
                        (974, 'Sparkling Wine - Rose, Freixenet', 'congue elementum in hac habitasse platea dictumst morbi vestibulum velit id pretium iaculis diam erat fermentum', 56.63, 66, '2020-08-07 00:00:00', 3, '-'),
                        (975, 'Galliano', 'semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero', 93.29, 90, '2021-01-29 00:00:00', 5, '-'),
                        (976, 'Passion Fruit', 'habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla', 64.48, 35, '2020-11-27 00:00:00', 4, '-'),
                        (977, 'Neckerchief Blck', 'eu interdum eu tincidunt in leo maecenas pulvinar lobortis est phasellus sit amet erat nulla tempus', 90.31, 100, '2020-07-14 00:00:00', 6, '-'),
                        (978, 'Sugar - Crumb', 'eget rutrum at lorem integer tincidunt ante vel ipsum praesent', 87.45, 0, '2021-02-17 00:00:00', 6, '-'),
                        (979, 'Oats Large Flake', 'tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis', 53.35, 82, '2020-09-17 00:00:00', 3, '-'),
                        (980, 'Gelatine Leaves - Envelopes', 'orci mauris lacinia sapien quis libero nullam sit amet turpis elementum ligula vehicula consequat', 74.18, 91, '2020-11-19 00:00:00', 5, '-'),
                        (981, 'Chicken - Leg / Back Attach', 'neque vestibulum eget vulputate ut ultrices vel augue vestibulum ante ipsum primis in faucibus orci', 54.26, 65, '2020-08-12 00:00:00', 3, '-'),
                        (982, 'Cheese - Comte', 'curabitur at ipsum ac tellus semper interdum mauris ullamcorper purus sit amet nulla quisque', 75.97, 42, '2020-09-08 00:00:00', 3, '-'),
                        (983, 'Vinegar - Champagne', 'nulla dapibus dolor vel est donec odio justo sollicitudin ut suscipit', 86.92, 81, '2020-06-20 00:00:00', 5, '-'),
                        (984, 'Kiwi', 'nascetur ridiculus mus etiam vel augue vestibulum rutrum rutrum neque aenean', 79.46, 99, '2021-02-24 00:00:00', 6, '-'),
                        (985, 'Kohlrabi', 'est congue elementum in hac habitasse platea dictumst morbi vestibulum velit id pretium', 48.16, 77, '2021-03-12 00:00:00', 3, '-'),
                        (986, 'Brandy Cherry - Mcguinness', 'ac nibh fusce lacus purus aliquet at feugiat non pretium quis lectus', 9.64, 57, '2021-01-20 00:00:00', 3, '-'),
                        (987, 'Sultanas', 'sed accumsan felis ut at dolor quis odio consequat varius integer ac leo pellentesque ultrices mattis odio donec', 62.10, 1, '2020-06-20 00:00:00', 3, '-'),
                        (988, 'V8 - Berry Blend', 'ipsum ac tellus semper interdum mauris ullamcorper purus sit amet nulla quisque arcu libero rutrum ac lobortis vel dapibus at', 15.77, 64, '2020-07-16 00:00:00', 5, '-'),
                        (989, 'Soup - Campbells, Creamy', 'pharetra magna vestibulum aliquet ultrices erat tortor sollicitudin mi sit amet lobortis sapien sapien non', 22.70, 30, '2021-01-06 00:00:00', 3, '-'),
                        (990, 'Creamers - 10%', 'suspendisse potenti in eleifend quam a odio in hac habitasse platea dictumst maecenas ut massa', 71.17, 53, '2021-01-05 00:00:00', 5, '-'),
                        (991, 'Mushroom - Porcini, Dry', 'turpis sed ante vivamus tortor duis mattis egestas metus aenean fermentum donec ut mauris eget massa tempor', 41.43, 36, '2020-07-08 00:00:00', 4, '-'),
                        (992, 'Cake - Miini Cheesecake Cherry', 'lacinia eget tincidunt eget tempus vel pede morbi porttitor lorem id ligula', 53.99, 59, '2020-10-27 00:00:00', 6, '-'),
                        (993, 'Carbonated Water - Raspberry', 'proin eu mi nulla ac enim in tempor turpis nec euismod scelerisque quam turpis adipiscing lorem vitae mattis', 32.22, 51, '2021-04-20 00:00:00', 3, '-'),
                        (994, 'Cream Of Tartar', 'sed sagittis nam congue risus semper porta volutpat quam pede lobortis ligula sit amet eleifend', 35.22, 44, '2020-08-31 00:00:00', 4, '-'),
                        (995, 'Club Soda - Schweppes, 355 Ml', 'sed tristique in tempus sit amet sem fusce consequat nulla nisl nunc nisl', 8.32, 61, '2021-03-19 00:00:00', 3, '-'),
                        (996, 'Beef - Rib Roast, Capless', 'sem sed sagittis nam congue risus semper porta volutpat quam pede lobortis ligula sit amet eleifend pede libero quis orci', 52.90, 68, '2020-06-20 00:00:00', 6, '-'),
                        (997, 'Salt - Table', 'etiam justo etiam pretium iaculis justo in hac habitasse platea dictumst etiam faucibus cursus urna ut tellus nulla ut erat', 37.51, 7, '2021-05-02 00:00:00', 6, '-'),
                        (998, 'Muffin Hinge 117n', 'mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus metus arcu adipiscing molestie hendrerit at vulputate', 59.84, 98, '2020-06-29 00:00:00', 3, '-'),
                        (999, 'Chicken - Wieners', 'eget tempus vel pede morbi porttitor lorem id ligula suspendisse ornare', 58.57, 5, '2020-08-16 00:00:00', 6, '-'),
                        (1000, 'Dried Peach', 'in faucibus orci luctus et ultrices posuere cubilia curae nulla dapibus dolor vel est donec odio justo sollicitudin', 41.22, 39, '2020-12-12 00:00:00', 4, '-');
            ''',
            '''
                insert into store_customer (id, first_name, last_name, membership) values (1, 'Boyd', 'Waltering', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (2, 'Davin', 'Calverd', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (3, 'Gamaliel', 'Lillow', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (4, 'Keslie', 'Slyme', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (5, 'Elwood', 'Clee', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (6, 'Friedrick', 'Dance', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (7, 'Wallis', 'Nurden', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (8, 'Marcella', 'Tribe', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (9, 'Talyah', 'Haydney', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (10, 'Fan', 'O''Moylane', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (11, 'Mikaela', 'Tulloch', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (12, 'Christiano', 'Piborn', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (13, 'Tiena', 'Swatton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (14, 'Christine', 'Cotter', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (15, 'Sada', 'Foad', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (16, 'Catriona', 'Simeone', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (17, 'Felisha', 'Cunningham', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (18, 'Aili', 'Botger', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (19, 'Janice', 'Frear', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (20, 'Brande', 'Humm', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (21, 'Murry', 'Sarfass', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (22, 'Sheilah', 'Unstead', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (23, 'Katrina', 'Goosey', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (24, 'Clevey', 'Tosspell', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (25, 'Stanislaw', 'Baldry', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (26, 'Berke', 'Bowick', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (27, 'Bernadene', 'Brewer', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (28, 'Karia', 'Whiffen', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (29, 'Phillis', 'Morecomb', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (30, 'Julina', 'Menear', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (31, 'Gretna', 'Coucher', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (32, 'Faber', 'Bunch', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (33, 'Darwin', 'Bulcock', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (34, 'Immanuel', 'Farrants', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (35, 'Errick', 'Lorkins', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (36, 'Cordie', 'Wonham', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (37, 'Verile', 'Dudeney', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (38, 'Rancell', 'Cockhill', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (39, 'Connor', 'Clery', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (40, 'Sigfried', 'Kepe', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (41, 'Ninette', 'Stranks', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (42, 'Veronica', 'Nansom', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (43, 'Jilli', 'Woolmer', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (44, 'Wilmar', 'Reast', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (45, 'Ev', 'Croke', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (46, 'Odele', 'Mohring', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (47, 'Gilemette', 'Petracci', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (48, 'Giordano', 'Higbin', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (49, 'Corette', 'Strognell', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (50, 'Ulrica', 'Donaghie', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (51, 'Pansie', 'Hugli', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (52, 'Deedee', 'Kennan', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (53, 'Martha', 'Tooting', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (54, 'Melamie', 'Grubb', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (55, 'Bianca', 'Dundendale', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (56, 'Tedmund', 'Hart', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (57, 'Melessa', 'Ianilli', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (58, 'Carter', 'Bertenshaw', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (59, 'Rad', 'Guare', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (60, 'Marylinda', 'Hawney', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (61, 'Aggy', 'Marcinkus', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (62, 'Jenelle', 'Toler', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (63, 'Moore', 'Hesbrook', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (64, 'Annemarie', 'Whacket', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (65, 'Jenifer', 'Humbles', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (66, 'Kristel', 'Ferney', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (67, 'Loretta', 'Mayzes', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (68, 'Roseanna', 'Mellenby', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (69, 'Garv', 'Melvin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (70, 'Franny', 'Ferenczi', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (71, 'Doll', 'Kubalek', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (72, 'Rockey', 'MacCathay', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (73, 'Stevana', 'Bruyns', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (74, 'Laetitia', 'Dudeney', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (75, 'Arney', 'Dicker', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (76, 'Rowland', 'Jeakins', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (77, 'Cyrille', 'Reeveley', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (78, 'Miller', 'Nettle', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (79, 'Obadias', 'Plessing', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (80, 'Conny', 'Gorman', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (81, 'Kristien', 'Ossipenko', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (82, 'Nevsa', 'Battisson', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (83, 'Dory', 'Dono', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (84, 'Lin', 'Fulger', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (85, 'Anastasia', 'Vasile', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (86, 'Melba', 'MacCague', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (87, 'Cherice', 'Townes', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (88, 'Ethelin', 'McQueen', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (89, 'Atlanta', 'Vondra', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (90, 'Jobi', 'Bollini', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (91, 'Malissa', 'Willock', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (92, 'Hyacinthie', 'Booler', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (93, 'Ulric', 'Strewthers', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (94, 'Ruddie', 'Baddam', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (95, 'Leonhard', 'Soffe', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (96, 'Derwin', 'Heazel', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (97, 'Richie', 'Kibby', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (98, 'Gail', 'Sumers', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (99, 'Nicolea', 'Arrighini', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (100, 'Hobey', 'Huffey', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (101, 'Saudra', 'Cutajar', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (102, 'Carlos', 'Woofendell', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (103, 'Nappy', 'Turbill', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (104, 'Tadeo', 'Ricart', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (105, 'Alisa', 'McIlrath', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (106, 'Mord', 'Tilio', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (107, 'Darcee', 'Lamblin', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (108, 'Karia', 'Roberti', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (109, 'Audre', 'Dixon', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (110, 'Jeno', 'Benardette', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (111, 'Farlie', 'Woollard', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (112, 'Vina', 'Watkiss', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (113, 'Nikolos', 'Minister', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (114, 'Jeannine', 'Schollar', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (115, 'Horatio', 'Worstall', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (116, 'Tore', 'Palister', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (117, 'Quinton', 'Scollan', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (118, 'Nevins', 'Jagoe', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (119, 'Aurelia', 'de la Valette Parisot', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (120, 'Tobie', 'Sillick', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (121, 'Dede', 'Avarne', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (122, 'Huntlee', 'McKie', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (123, 'Brew', 'Gruby', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (124, 'Conny', 'Warrilow', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (125, 'Joell', 'Riceards', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (126, 'Aldo', 'Bartak', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (127, 'Lorette', 'Soffe', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (128, 'Trula', 'Fallawe', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (129, 'Lindi', 'Sturdy', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (130, 'Edgard', 'Moohan', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (131, 'Andras', 'Idenden', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (132, 'Julietta', 'Boseley', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (133, 'Shannon', 'McGonagle', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (134, 'Cymbre', 'Toppin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (135, 'Estelle', 'Gladtbach', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (136, 'Archaimbaud', 'Cullity', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (137, 'Moishe', 'Grinsdale', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (138, 'Wilek', 'Blanket', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (139, 'Esteban', 'Clemot', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (140, 'Corissa', 'Stanistreet', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (141, 'Meyer', 'Leatherborrow', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (142, 'Lebbie', 'Crabbe', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (143, 'Lars', 'Garrand', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (144, 'Celestyn', 'Saby', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (145, 'Tonya', 'Carvil', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (146, 'Frans', 'Eccleshare', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (147, 'Aldwin', 'Ruddiforth', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (148, 'Jack', 'MacHarg', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (149, 'Ezra', 'Fydoe', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (150, 'Audra', 'Baunton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (151, 'Guthrie', 'Dibnah', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (152, 'Pepi', 'Goodbar', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (153, 'Appolonia', 'Flintoff', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (154, 'Milena', 'Faughey', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (155, 'Rolfe', 'Elmhurst', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (156, 'Maible', 'Seckom', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (157, 'Hi', 'Hedgeley', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (158, 'Matty', 'Pagin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (159, 'Kale', 'Thandi', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (160, 'Georgie', 'Buche', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (161, 'Iggy', 'Buckell', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (162, 'Olvan', 'Iczokvitz', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (163, 'Derwin', 'Robak', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (164, 'Aurelie', 'Saldler', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (165, 'Pennie', 'Burling', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (166, 'Felicdad', 'Pankhurst.', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (167, 'Laverna', 'Aylett', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (168, 'Tybalt', 'Martonfi', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (169, 'Robb', 'Paulitschke', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (170, 'Garvy', 'Instock', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (171, 'Ramonda', 'Shawdforth', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (172, 'Cammy', 'Howlett', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (173, 'Matilda', 'Linnett', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (174, 'Hyacintha', 'Corlett', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (175, 'Mozelle', 'Wilder', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (176, 'Tamiko', 'Salvador', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (177, 'Etheline', 'Tidbury', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (178, 'Jere', 'Blazdell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (179, 'Reine', 'Raynham', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (180, 'Linnea', 'Drysdell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (181, 'Yuri', 'Stoyles', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (182, 'Linda', 'Moloney', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (183, 'Addi', 'Ambridge', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (184, 'Benjamin', 'Ricks', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (185, 'Dorolice', 'Mowsdell', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (186, 'Wylma', 'Deam', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (187, 'Merell', 'Slimon', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (188, 'Isidor', 'Pull', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (189, 'Isaak', 'Sarjeant', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (190, 'Munroe', 'Glassford', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (191, 'Cyndi', 'Edgeley', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (192, 'Myer', 'Mourant', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (193, 'Barty', 'Roon', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (194, 'Viola', 'Nicholas', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (195, 'Westleigh', 'Durrance', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (196, 'Marylinda', 'Simeoli', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (197, 'Urbanus', 'Charlot', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (198, 'Elvin', 'Tassel', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (199, 'Kara', 'Rosettini', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (200, 'Ailbert', 'Lacoste', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (201, 'Almeria', 'Huxtable', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (202, 'Matthaeus', 'Berg', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (203, 'Terrance', 'Gawthorp', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (204, 'Happy', 'Felkin', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (205, 'Morlee', 'MacCartan', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (206, 'Frazier', 'Probyn', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (207, 'Lothaire', 'Sach', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (208, 'Kerianne', 'Strutley', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (209, 'Trip', 'Nolleau', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (210, 'Alfie', 'Doorbar', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (211, 'Bebe', 'Edmonds', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (212, 'George', 'Sorton', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (213, 'Caralie', 'Haps', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (214, 'Kaiser', 'Leathers', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (215, 'Helen', 'Maher', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (216, 'Zane', 'Hukin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (217, 'Pedro', 'Stoodley', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (218, 'Domenic', 'Fewell', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (219, 'Anne-marie', 'Corriea', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (220, 'Denice', 'Belison', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (221, 'Marietta', 'Scroxton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (222, 'Winnifred', 'Merriment', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (223, 'Tabby', 'Bonds', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (224, 'Robin', 'Gavrieli', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (225, 'Antonina', 'Fotitt', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (226, 'Stafford', 'Vasilchikov', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (227, 'Rowland', 'Dibdin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (228, 'Danie', 'Laughrey', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (229, 'Colman', 'Ickowicz', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (230, 'Milton', 'Klossek', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (231, 'Katey', 'Comoletti', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (232, 'Brita', 'Aleshintsev', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (233, 'Elladine', 'Birdwhistle', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (234, 'Alvira', 'Allin', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (235, 'Ashlie', 'Leonards', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (236, 'Danielle', 'Skace', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (237, 'Tanitansy', 'Dagg', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (238, 'Cam', 'Flatley', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (239, 'Joaquin', 'Werendell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (240, 'Winona', 'Botham', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (241, 'Robbin', 'Benck', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (242, 'Kelcie', 'Kingham', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (243, 'Retha', 'Ricardin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (244, 'Clareta', 'Truesdale', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (245, 'Georgia', 'Sebrook', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (246, 'Bee', 'Geeves', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (247, 'Charline', 'Skamell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (248, 'Leonid', 'Custard', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (249, 'Saunderson', 'Chinge', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (250, 'Wayne', 'Raulstone', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (251, 'Lacey', 'Lumsdale', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (252, 'Ofella', 'Cant', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (253, 'Debee', 'MacDermid', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (254, 'Giff', 'Risdall', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (255, 'Austen', 'Tomek', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (256, 'Marlon', 'Tuxwell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (257, 'Jerry', 'Rittmeyer', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (258, 'Charlot', 'Eagell', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (259, 'Nedda', 'Pillman', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (260, 'Maud', 'Sutch', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (261, 'Xylia', 'Flint', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (262, 'Jilli', 'Turn', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (263, 'Laetitia', 'Kerkham', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (264, 'Lishe', 'Desbrow', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (265, 'Donal', 'Upchurch', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (266, 'Reade', 'Bransdon', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (267, 'Charlot', 'Swayne', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (268, 'Dunstan', 'Dudley', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (269, 'Fedora', 'Delieu', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (270, 'Eimile', 'Wigan', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (271, 'Fabian', 'Alexandersen', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (272, 'Pia', 'Scrivinor', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (273, 'Shena', 'Smerdon', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (274, 'Lina', 'Davidovitch', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (275, 'Kevin', 'Olenchikov', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (276, 'Raffaello', 'Jardine', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (277, 'Fraser', 'Tegeller', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (278, 'Frasco', 'Ca', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (279, 'Linnell', 'Yurkov', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (280, 'Clyve', 'Knifton', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (281, 'Maximilian', 'Gurnell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (282, 'Dag', 'Layhe', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (283, 'Iolanthe', 'McGinn', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (284, 'Vanessa', 'Betts', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (285, 'Sherwin', 'Vinick', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (286, 'Burtie', 'McManus', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (287, 'Casi', 'Licciardiello', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (288, 'Jobi', 'Neild', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (289, 'Carter', 'Ivkovic', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (290, 'Baudoin', 'Bault', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (291, 'Katusha', 'Duckers', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (292, 'Lucienne', 'Jillions', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (293, 'Krista', 'Elies', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (294, 'Maddie', 'Charrington', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (295, 'Bobbi', 'Zanelli', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (296, 'Orlando', 'McCalum', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (297, 'Cornela', 'Carek', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (298, 'Dunstan', 'Brayson', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (299, 'Clemence', 'Skyram', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (300, 'Dorrie', 'Barchrameev', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (301, 'Vikky', 'Bortoloni', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (302, 'Simone', 'Stoite', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (303, 'Faber', 'Greason', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (304, 'Borden', 'Scutter', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (305, 'Aube', 'Tumayan', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (306, 'Heinrik', 'Wem', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (307, 'Drusie', 'Blinkhorn', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (308, 'Ezechiel', 'Iacivelli', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (309, 'Baird', 'Crotch', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (310, 'Jeanna', 'Broseman', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (311, 'Callida', 'Domnin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (312, 'Terrell', 'MacCarlich', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (313, 'Fleur', 'Trainer', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (314, 'Noach', 'Sager', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (315, 'Ringo', 'Karus', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (316, 'Blakeley', 'Blackster', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (317, 'Katherina', 'Alonso', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (318, 'Marcello', 'Misson', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (319, 'Theodoric', 'Clapston', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (320, 'Bret', 'Moorton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (321, 'Sapphira', 'Wibrew', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (322, 'Gwenore', 'Haryngton', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (323, 'Lanita', 'Waddup', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (324, 'Emmey', 'Robottham', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (325, 'Mickie', 'Doutch', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (326, 'Zuzana', 'Monson', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (327, 'Kordula', 'Quainton', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (328, 'Shellie', 'Bunstone', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (329, 'Addy', 'Ivashkin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (330, 'Curtice', 'Molloy', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (331, 'Nelie', 'Cancott', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (332, 'Karisa', 'Eloy', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (333, 'Georgi', 'Adolthine', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (334, 'Mella', 'Cartmill', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (335, 'Far', 'Lampart', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (336, 'Kanya', 'Marusik', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (337, 'Markos', 'Manach', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (338, 'Orlando', 'Wingfield', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (339, 'Kathrine', 'Cleland', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (340, 'Damara', 'Cowherd', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (341, 'Janessa', 'Floweth', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (342, 'Dione', 'Matz', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (343, 'Lanna', 'Antonescu', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (344, 'Walton', 'Tutill', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (345, 'Christalle', 'Ploughwright', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (346, 'Beverlie', 'Stickler', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (347, 'Dona', 'Mitford', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (348, 'Petronilla', 'Janaway', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (349, 'Barnabas', 'Clerc', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (350, 'Vikky', 'Turfin', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (351, 'Oliy', 'Zukerman', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (352, 'Maressa', 'Featley', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (353, 'Colly', 'Stares', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (354, 'Toddy', 'Caro', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (355, 'Mathe', 'Normansell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (356, 'Amanda', 'Ruddom', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (357, 'Dion', 'Kermon', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (358, 'Clareta', 'Fossord', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (359, 'Zabrina', 'Brideoke', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (360, 'Alair', 'Lafflina', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (361, 'Batsheva', 'Kopacek', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (362, 'Conant', 'Blues', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (363, 'Franky', 'Colman', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (364, 'Wren', 'Golder', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (365, 'Norry', 'Godridge', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (366, 'Norton', 'Shelbourne', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (367, 'Eugenie', 'Sessuns', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (368, 'Montgomery', 'Broe', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (369, 'Madelin', 'Inger', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (370, 'Riane', 'Pitherick', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (371, 'Manon', 'Coady', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (372, 'Kendall', 'Ruckman', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (373, 'Wylie', 'Giacaponi', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (374, 'Malynda', 'Rasch', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (375, 'Ariana', 'Lanahan', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (376, 'Dyana', 'Tumilson', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (377, 'Bernette', 'Jaskiewicz', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (378, 'Celestine', 'Trobridge', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (379, 'Margalo', 'Cooling', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (380, 'Wyn', 'Fieldhouse', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (381, 'Keen', 'O''Curneen', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (382, 'Shani', 'Tann', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (383, 'Dion', 'Fox', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (384, 'Kerby', 'Baroch', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (385, 'Shannan', 'O''Gormley', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (386, 'Reamonn', 'Exposito', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (387, 'Rubina', 'Ellings', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (388, 'Margarethe', 'Ubank', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (389, 'Jacquetta', 'Sanches', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (390, 'Evaleen', 'Seint', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (391, 'Stu', 'Youel', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (392, 'Aileen', 'de Chastelain', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (393, 'Kerrie', 'Giordano', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (394, 'Carling', 'Cale', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (395, 'Julieta', 'March', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (396, 'Oby', 'Abby', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (397, 'Eleni', 'Shewry', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (398, 'Ariadne', 'Blenkharn', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (399, 'Joachim', 'Davidofski', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (400, 'Xena', 'Archley', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (401, 'Claresta', 'Follacaro', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (402, 'Flore', 'Scown', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (403, 'Brew', 'Lavies', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (404, 'Brana', 'Tidbold', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (405, 'Mame', 'Ralfe', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (406, 'Maude', 'Hanfrey', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (407, 'Bogey', 'Matfield', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (408, 'Kassi', 'Dumbelton', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (409, 'Boyd', 'Turpie', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (410, 'Erie', 'Pyper', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (411, 'Tedd', 'Kernley', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (412, 'Rodney', 'Mattusevich', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (413, 'Shawn', 'Rudwell', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (414, 'Rosalie', 'Koeppke', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (415, 'Hamnet', 'Lambdon', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (416, 'Meta', 'Pridie', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (417, 'Iseabal', 'Salkeld', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (418, 'Forest', 'Shuker', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (419, 'Bartholomeus', 'Figgess', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (420, 'Marty', 'Andryushchenko', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (421, 'Barri', 'Cregeen', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (422, 'Tiena', 'Kitchaside', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (423, 'Portia', 'Trevor', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (424, 'Gilligan', 'Duggon', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (425, 'Gus', 'Renvoise', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (426, 'Raymond', 'Percy', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (427, 'Jordan', 'Becraft', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (428, 'Harmony', 'Stiegers', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (429, 'Faustina', 'Fader', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (430, 'Stephanie', 'Nesbit', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (431, 'Laure', 'Lovat', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (432, 'Harmony', 'Ogle', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (433, 'Andras', 'Ormond', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (434, 'Ronny', 'Crump', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (435, 'Kerstin', 'Berrie', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (436, 'Joela', 'Dredge', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (437, 'Friederike', 'Ansett', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (438, 'Ulrica', 'Crystal', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (439, 'Norene', 'Joblin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (440, 'Darya', 'Lambkin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (441, 'Hannah', 'Remon', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (442, 'Ario', 'O''Dare', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (443, 'Robbin', 'Dudhill', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (444, 'Vin', 'Francomb', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (445, 'Gregorius', 'Hundy', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (446, 'Deeann', 'Gorling', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (447, 'Bobbie', 'Pappi', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (448, 'Lyman', 'Follos', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (449, 'Anett', 'Rankcom', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (450, 'Lemmie', 'Schroeder', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (451, 'Brietta', 'Beurich', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (452, 'Everett', 'Cherry Holme', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (453, 'Darleen', 'Josefer', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (454, 'Bowie', 'McConnachie', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (455, 'Emma', 'Sempill', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (456, 'Gregory', 'Yurkov', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (457, 'Forest', 'Astbery', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (458, 'Gregorius', 'Sone', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (459, 'Cordy', 'Theriot', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (460, 'Gabbie', 'Pellingar', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (461, 'Danyelle', 'Farrow', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (462, 'Mabelle', 'Kirsz', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (463, 'Lorenzo', 'Heustace', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (464, 'Niccolo', 'Swatman', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (465, 'Kelby', 'Le Clercq', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (466, 'Willi', 'Fearn', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (467, 'Quintus', 'Yewman', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (468, 'Boycey', 'Kretschmer', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (469, 'Kizzie', 'Worsnup', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (470, 'Jessie', 'Pentecost', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (471, 'Edwin', 'Eves', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (472, 'Adriana', 'Vedyashkin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (473, 'Cissiee', 'Hrishanok', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (474, 'Briano', 'Lerwell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (475, 'Micky', 'Wrightham', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (476, 'Celia', 'Baribal', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (477, 'Ilario', 'Sullly', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (478, 'Demetrius', 'Tardiff', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (479, 'Herve', 'Veal', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (480, 'Ellary', 'Groven', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (481, 'Joya', 'O'' Liddy', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (482, 'Dyan', 'Hardman', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (483, 'Domeniga', 'Addyman', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (484, 'Cathryn', 'Northway', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (485, 'Oran', 'Laterza', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (486, 'Brenda', 'Carff', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (487, 'Lisetta', 'Huggan', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (488, 'Teodoro', 'Janoschek', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (489, 'Nelia', 'Berrisford', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (490, 'Phineas', 'Lawlie', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (491, 'Haily', 'Brehat', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (492, 'Gloria', 'Kenaway', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (493, 'Rozanna', 'Kettel', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (494, 'Legra', 'Forrestor', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (495, 'Martie', 'Maddison', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (496, 'Peggy', 'Thoms', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (497, 'Donny', 'Dalling', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (498, 'Pasquale', 'Sterndale', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (499, 'Domenic', 'Treat', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (500, 'Bevan', 'Bridson', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (501, 'Casi', 'Lapenna', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (502, 'Dani', 'Battie', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (503, 'Arnold', 'Alfonso', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (504, 'Krystyna', 'Cogle', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (505, 'Lia', 'Matieu', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (506, 'Lulita', 'Ludwikiewicz', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (507, 'Helge', 'Olivetti', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (508, 'Garrard', 'Flowitt', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (509, 'Georgie', 'Lidgerton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (510, 'Betteann', 'Otham', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (511, 'Myca', 'Syratt', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (512, 'Sascha', 'Leaming', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (513, 'Brew', 'Izsak', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (514, 'Luise', 'Wignall', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (515, 'Erastus', 'Guitel', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (516, 'Kirby', 'Rickards', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (517, 'Harrie', 'Ffrench', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (518, 'Amabelle', 'Daveran', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (519, 'Charlton', 'Forri', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (520, 'Bart', 'Rootham', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (521, 'Anne-corinne', 'Nend', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (522, 'Fara', 'Landrean', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (523, 'Mei', 'Soles', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (524, 'Chandal', 'Hirche', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (525, 'Krissy', 'Edleston', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (526, 'Ellwood', 'Dimitrijevic', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (527, 'Bettye', 'Hammer', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (528, 'Corina', 'Willoughby', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (529, 'Ginger', 'Lefridge', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (530, 'Umberto', 'Ballendine', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (531, 'Vivyan', 'Limb', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (532, 'Burty', 'Draper', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (533, 'Denise', 'Monro', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (534, 'Dareen', 'Kellen', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (535, 'Merle', 'Trower', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (536, 'Christian', 'Kemmish', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (537, 'Merlina', 'Smeal', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (538, 'Peg', 'Lugton', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (539, 'Hebert', 'Clerc', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (540, 'Ronica', 'Adaway', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (541, 'Waylin', 'Bransby', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (542, 'Tildi', 'Bleakley', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (543, 'Raven', 'Villar', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (544, 'Caitrin', 'Gumly', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (545, 'Heida', 'Tapply', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (546, 'Corabel', 'Tuplin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (547, 'Kalindi', 'Willoughby', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (548, 'Gannie', 'Zapater', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (549, 'Sergei', 'Imlach', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (550, 'Devonne', 'Angier', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (551, 'Saree', 'Millichip', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (552, 'Teriann', 'Tedahl', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (553, 'Mordecai', 'Leetham', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (554, 'Deny', 'Havercroft', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (555, 'Cherise', 'Jensen', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (556, 'Maurie', 'McGeown', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (557, 'Jacquenetta', 'Jerzyk', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (558, 'Clarabelle', 'Staples', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (559, 'Danila', 'Ranklin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (560, 'Tamar', 'Kilpin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (561, 'Terese', 'Geockle', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (562, 'Charmain', 'Jackman', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (563, 'Marcy', 'Pescott', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (564, 'Gail', 'Euler', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (565, 'Emiline', 'Ruhben', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (566, 'Dori', 'Rushmer', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (567, 'Homer', 'Smithson', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (568, 'Adey', 'Dankov', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (569, 'Angelika', 'Mosconi', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (570, 'Dinah', 'Nend', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (571, 'Duky', 'Cubuzzi', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (572, 'Micaela', 'Fernihough', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (573, 'Odey', 'Oxford', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (574, 'Andris', 'Giaomozzo', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (575, 'Derrick', 'Klagge', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (576, 'Durant', 'Exrol', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (577, 'Keven', 'Cathie', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (578, 'Lawton', 'Kivelhan', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (579, 'Cass', 'Creamen', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (580, 'Owen', 'Rallings', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (581, 'Jannelle', 'Haldenby', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (582, 'Cherin', 'Jeannequin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (583, 'Shandeigh', 'Kohter', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (584, 'Howard', 'Newns', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (585, 'Murdock', 'O''Collopy', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (586, 'Lezlie', 'Dugood', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (587, 'Marcella', 'De Marchi', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (588, 'Consuela', 'Sollas', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (589, 'Marcelia', 'Starbuck', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (590, 'Ira', 'Fance', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (591, 'Shawna', 'Paddemore', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (592, 'Stevana', 'Fishbourn', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (593, 'Christabel', 'Branni', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (594, 'Benita', 'Loads', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (595, 'Bridget', 'Whitsey', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (596, 'Leighton', 'Sleath', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (597, 'Anderson', 'Oxley', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (598, 'Stanton', 'McIlvoray', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (599, 'Brian', 'Blaymires', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (600, 'Broderick', 'Ramsell', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (601, 'Haskel', 'Fanton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (602, 'Abbey', 'Pattle', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (603, 'Petronilla', 'Hofler', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (604, 'Flossi', 'Marquess', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (605, 'Marmaduke', 'Vint', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (606, 'Binky', 'Glazebrook', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (607, 'Candra', 'Passo', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (608, 'Fawn', 'McCoole', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (609, 'Velvet', 'Hamilton', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (610, 'Sheffie', 'Wallbank', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (611, 'Bendix', 'Mapis', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (612, 'Hunfredo', 'Francklin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (613, 'Trude', 'Daniau', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (614, 'Garrick', 'Murrhardt', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (615, 'Ange', 'Massot', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (616, 'Mady', 'Gut', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (617, 'Al', 'Pickburn', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (618, 'Lana', 'Copland', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (619, 'Di', 'Swapp', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (620, 'Ron', 'Looker', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (621, 'Jake', 'Jeaneau', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (622, 'Benoite', 'O'' Clovan', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (623, 'Forbes', 'Knox', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (624, 'Gallagher', 'Bene', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (625, 'Noell', 'Nijs', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (626, 'Shaylah', 'Davidowsky', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (627, 'Arlyn', 'Matasov', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (628, 'Kort', 'Crufts', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (629, 'Annabella', 'Gordge', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (630, 'Marlow', 'Blazi', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (631, 'Russell', 'Johnson', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (632, 'Lise', 'Burras', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (633, 'Melesa', 'Prazer', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (634, 'Joy', 'Swinfen', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (635, 'Christine', 'Iglesiaz', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (636, 'Hailey', 'Otley', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (637, 'Arlene', 'Stockey', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (638, 'Harland', 'Dayer', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (639, 'Rodrick', 'Grishenkov', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (640, 'Kaila', 'Dukelow', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (641, 'Merrel', 'Blackston', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (642, 'August', 'Johnston', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (643, 'Hillary', 'Klimshuk', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (644, 'Issi', 'O''Lunny', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (645, 'Andreas', 'Pickersgill', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (646, 'Mirilla', 'Crawford', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (647, 'Helene', 'Halhead', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (648, 'Sylvester', 'Renn', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (649, 'Carolin', 'Dener', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (650, 'Etty', 'Berdale', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (651, 'Alayne', 'Tertre', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (652, 'Maryanne', 'Howship', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (653, 'Krystle', 'Danes', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (654, 'Ambros', 'Obal', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (655, 'Hugibert', 'Philippault', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (656, 'Evy', 'Shirtliff', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (657, 'Fiona', 'Clausius', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (658, 'Ileana', 'Towns', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (659, 'Jyoti', 'Mander', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (660, 'Zarla', 'McCromley', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (661, 'Aurel', 'Graveney', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (662, 'Brade', 'Woodes', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (663, 'Margot', 'Tabourier', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (664, 'Gisella', 'Firpi', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (665, 'Derrek', 'Rubertis', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (666, 'Dru', 'Woodfin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (667, 'Lexis', 'Glentz', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (668, 'Merilee', 'Illidge', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (669, 'Derwin', 'Jeannin', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (670, 'Lavina', 'Gircke', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (671, 'Orel', 'Ferroli', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (672, 'Chelsae', 'Elbourn', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (673, 'Paulina', 'Alexsandrowicz', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (674, 'Ramon', 'Copin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (675, 'Ami', 'Capey', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (676, 'Emmy', 'Cruickshanks', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (677, 'Rafferty', 'Stainbridge', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (678, 'Elia', 'Skedgell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (679, 'Orran', 'Da Costa', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (680, 'Fanni', 'Jumont', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (681, 'Luisa', 'Fishley', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (682, 'Xever', 'Boughey', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (683, 'Fletch', 'Gilhool', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (684, 'Jillian', 'Jiroutek', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (685, 'Orazio', 'Giacobilio', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (686, 'Maressa', 'Hanhardt', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (687, 'Thane', 'Durnall', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (688, 'Norrie', 'Boleyn', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (689, 'Lauritz', 'Giriardelli', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (690, 'Aguste', 'Ovendale', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (691, 'Karoline', 'Edgerly', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (692, 'Rahal', 'Pikhno', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (693, 'Ella', 'Edmunds', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (694, 'Angil', 'Johannes', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (695, 'Marianna', 'Bendall', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (696, 'Eimile', 'Durrand', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (697, 'Carroll', 'Leaves', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (698, 'Shanon', 'MacDonell', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (699, 'Ashien', 'Stenyng', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (700, 'Alexandro', 'Gounard', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (701, 'Lynne', 'Pattemore', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (702, 'Dix', 'Doelle', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (703, 'Yardley', 'Cowing', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (704, 'Ariel', 'Norfolk', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (705, 'Kessia', 'Shorton', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (706, 'Marianna', 'Syred', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (707, 'Haywood', 'Arnli', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (708, 'Leontine', 'Stollen', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (709, 'Anthony', 'Fullager', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (710, 'Jewell', 'Condit', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (711, 'Katey', 'Glenfield', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (712, 'Gonzalo', 'Olivie', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (713, 'Eliza', 'Vegas', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (714, 'Constancy', 'Preble', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (715, 'Linnea', 'Czadla', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (716, 'Ardeen', 'Filan', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (717, 'Danya', 'McEvilly', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (718, 'Babbie', 'Drillingcourt', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (719, 'Larry', 'Campbell-Dunlop', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (720, 'Elvyn', 'Maric', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (721, 'Frederico', 'Accombe', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (722, 'Jeralee', 'Rama', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (723, 'Xavier', 'Thorbon', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (724, 'Willy', 'Moynham', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (725, 'Dido', 'Esslemont', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (726, 'Larisa', 'Braghini', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (727, 'Toddy', 'Denniss', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (728, 'Blinny', 'Gummie', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (729, 'Eliza', 'Mabone', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (730, 'Omar', 'Edwardson', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (731, 'Ashley', 'Dummigan', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (732, 'Tristam', 'Chate', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (733, 'Stefan', 'Trigwell', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (734, 'Russell', 'Tembridge', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (735, 'Hailey', 'Follin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (736, 'Keen', 'Chimienti', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (737, 'Mahala', 'Belli', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (738, 'Justinian', 'Alywin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (739, 'Sharai', 'Ruf', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (740, 'Lionello', 'Withur', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (741, 'Nariko', 'Mc Menamin', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (742, 'Elfreda', 'Gibbeson', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (743, 'Flinn', 'Suttling', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (744, 'Rina', 'Beagin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (745, 'Si', 'Bakewell', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (746, 'Tammara', 'Christofor', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (747, 'Arney', 'Feldberger', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (748, 'Ahmad', 'Laweles', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (749, 'Olvan', 'Harp', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (750, 'Stephana', 'Breede', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (751, 'Leesa', 'Halgarth', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (752, 'Lonnard', 'Biasini', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (753, 'Saree', 'Thurlborn', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (754, 'Lindsay', 'Gaveltone', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (755, 'Dierdre', 'Reuben', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (756, 'Shir', 'Pinchback', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (757, 'Grenville', 'Braben', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (758, 'Phineas', 'Grece', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (759, 'Lou', 'Seivertsen', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (760, 'Garret', 'Court', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (761, 'Orsa', 'Gayton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (762, 'Mannie', 'Castiblanco', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (763, 'Magda', 'Dodgson', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (764, 'Kennedy', 'Wing', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (765, 'Roi', 'Genike', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (766, 'George', 'Vearnals', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (767, 'Glen', 'Tomas', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (768, 'Giacinta', 'Pottle', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (769, 'Shina', 'Beumant', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (770, 'Cherrita', 'Fetherston', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (771, 'Chad', 'Thiem', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (772, 'Dolf', 'Hubbis', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (773, 'Merell', 'McKie', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (774, 'Melvyn', 'Reneke', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (775, 'Elisha', 'Crosseland', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (776, 'Thatch', 'L''Amie', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (777, 'Staford', 'Eitter', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (778, 'Honor', 'Fedorchenko', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (779, 'Petronilla', 'Denzey', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (780, 'Dorry', 'Longea', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (781, 'Natka', 'Hodgen', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (782, 'Carroll', 'Durtnel', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (783, 'Wesley', 'Iozefovich', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (784, 'Annie', 'MacTerrelly', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (785, 'Bab', 'Tomalin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (786, 'Sawyer', 'Steanyng', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (787, 'Hi', 'Paulack', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (788, 'Ford', 'Cattenach', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (789, 'Tana', 'Annon', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (790, 'Hephzibah', 'Angus', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (791, 'Pryce', 'Chudleigh', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (792, 'Sallyann', 'Rait', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (793, 'Etheline', 'Deeley', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (794, 'Cherida', 'Woolaston', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (795, 'Lew', 'Boich', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (796, 'Lorilee', 'Harfleet', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (797, 'Ravi', 'Allden', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (798, 'Elysia', 'Corrado', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (799, 'Cathyleen', 'Kennet', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (800, 'Rhetta', 'Denford', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (801, 'Trstram', 'McOnie', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (802, 'Emma', 'Colafate', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (803, 'Gerladina', 'Bourgour', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (804, 'Neddie', 'Binner', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (805, 'Cello', 'Petow', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (806, 'Darryl', 'Trodd', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (807, 'Cross', 'Di Francecshi', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (808, 'Corie', 'Pontefract', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (809, 'Lauren', 'Bernhard', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (810, 'Josephina', 'Souness', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (811, 'Camel', 'Jeratt', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (812, 'Farleigh', 'O''Scollain', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (813, 'Grover', 'Stirgess', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (814, 'Fitz', 'Postin', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (815, 'Shep', 'Harrell', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (816, 'Dino', 'Moors', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (817, 'Gilles', 'Boshell', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (818, 'Anitra', 'Butts', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (819, 'Kittie', 'Zielinski', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (820, 'Haleigh', 'Philliphs', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (821, 'Mignonne', 'Witchalls', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (822, 'Pietrek', 'Shane', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (823, 'Shauna', 'McKean', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (824, 'Marylinda', 'Pardi', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (825, 'Lyell', 'Presnell', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (826, 'Clerc', 'Chetwind', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (827, 'Casandra', 'Bloy', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (828, 'Lemar', 'Moat', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (829, 'Wildon', 'Jahndel', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (830, 'Dare', 'Cleminson', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (831, 'Felic', 'Khristoforov', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (832, 'Suki', 'Josofovitz', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (833, 'Robinet', 'Kornyshev', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (834, 'Talbert', 'Hachette', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (835, 'Ruben', 'Budgeon', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (836, 'Evelyn', 'Soame', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (837, 'Tally', 'Sicily', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (838, 'Charyl', 'Whitbread', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (839, 'Tanney', 'Top', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (840, 'Balduin', 'Unworth', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (841, 'Michal', 'MacMeekan', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (842, 'Constantine', 'Memmory', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (843, 'Evelyn', 'Stallworth', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (844, 'Normie', 'Wiburn', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (845, 'Gertruda', 'Staterfield', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (846, 'Clevie', 'Alben', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (847, 'Filip', 'Stalley', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (848, 'Abbey', 'Haslin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (849, 'Alanson', 'Wanklyn', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (850, 'Wilma', 'Bussen', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (851, 'Ambros', 'Jordine', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (852, 'Welbie', 'Mateos', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (853, 'Pepito', 'Valentin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (854, 'Meade', 'McCleary', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (855, 'Hasheem', 'Cordel', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (856, 'Glynda', 'Slipper', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (857, 'Merilee', 'Ickov', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (858, 'Mirelle', 'Piggen', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (859, 'Read', 'McCumesky', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (860, 'Tybalt', 'O''Fallone', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (861, 'Sheffy', 'Phlipon', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (862, 'Danni', 'Wharlton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (863, 'Iggie', 'Shilling', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (864, 'Mortie', 'Cumberlidge', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (865, 'Robina', 'Benstead', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (866, 'Valida', 'Deverock', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (867, 'Crista', 'Proudman', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (868, 'Jesse', 'Caress', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (869, 'Sheffy', 'Thickins', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (870, 'Minta', 'Housiaux', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (871, 'Ailee', 'Lydiate', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (872, 'Fairlie', 'Todman', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (873, 'Padraic', 'Cardoo', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (874, 'Lothaire', 'Warman', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (875, 'Zandra', 'Brind', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (876, 'Jess', 'Lamplugh', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (877, 'Reena', 'Stebles', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (878, 'Sue', 'Eatherton', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (879, 'Danika', 'Moxsom', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (880, 'Ham', 'Eaken', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (881, 'Eartha', 'Wyatt', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (882, 'Blake', 'Webland', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (883, 'Adela', 'Bello', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (884, 'Georgina', 'Baroux', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (885, 'Godiva', 'Plumbridge', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (886, 'Thor', 'Spavins', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (887, 'Yard', 'Robins', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (888, 'Demetri', 'Lysons', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (889, 'Iggie', 'Chaudron', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (890, 'Myrtia', 'Syplus', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (891, 'Justine', 'Dungate', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (892, 'Zita', 'Petrazzi', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (893, 'Sharla', 'Hurnell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (894, 'Zacharie', 'Daid', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (895, 'Aliza', 'Reany', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (896, 'Ofella', 'Plumm', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (897, 'Maurits', 'St Clair', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (898, 'Stafford', 'Dumphries', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (899, 'Kelila', 'Daouze', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (900, 'Allen', 'Robert', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (901, 'Claudette', 'Shackle', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (902, 'Wallache', 'Triggel', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (903, 'Malissia', 'Stokell', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (904, 'Lesley', 'O''Mahoney', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (905, 'Idelle', 'Menichelli', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (906, 'Augustus', 'Stanfield', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (907, 'Dalli', 'Aleveque', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (908, 'Wyatt', 'Maykin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (909, 'Chastity', 'Di Antonio', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (910, 'Lothario', 'Maggill''Andreis', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (911, 'Wilfred', 'Grasha', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (912, 'Edsel', 'Huntington', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (913, 'Eden', 'Fenby', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (914, 'Ardine', 'Schreiner', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (915, 'Kacie', 'Callacher', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (916, 'Barthel', 'Conroy', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (917, 'Bryon', 'Livett', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (918, 'Charin', 'Bride', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (919, 'Anthea', 'Lilley', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (920, 'Yancey', 'Ritson', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (921, 'Haley', 'Christauffour', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (922, 'Giffy', 'Hindshaw', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (923, 'Lyndy', 'Winteringham', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (924, 'Richie', 'Gentle', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (925, 'Jonie', 'Skoof', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (926, 'Camey', 'Lancastle', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (927, 'Cori', 'Papen', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (928, 'Fabio', 'Pestor', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (929, 'Jacquelin', 'Cyples', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (930, 'Bertrando', 'Barsham', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (931, 'Janet', 'Crabtree', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (932, 'Garold', 'De Coursey', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (933, 'Seana', 'McLemon', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (934, 'Cathryn', 'Battleson', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (935, 'Maud', 'Alvarado', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (936, 'Shepard', 'Otley', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (937, 'Elayne', 'O'' Sullivan', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (938, 'Rici', 'Claussen', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (939, 'Elsi', 'Melmar', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (940, 'Vincent', 'Schult', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (941, 'Doralynne', 'Vondra', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (942, 'Teddy', 'Bhar', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (943, 'Beckie', 'Seale', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (944, 'Filippo', 'Navarijo', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (945, 'Kim', 'Neathway', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (946, 'Marsiella', 'Gonnely', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (947, 'Piotr', 'Duthie', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (948, 'Fallon', 'Crean', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (949, 'Hillie', 'Fatkin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (950, 'Reggie', 'Gasparro', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (951, 'Renie', 'Wortman', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (952, 'Estel', 'Shilito', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (953, 'Adina', 'Tinston', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (954, 'Heriberto', 'Evennett', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (955, 'Rozina', 'Dixey', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (956, 'Franklyn', 'Clarson', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (957, 'Benny', 'Minnis', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (958, 'Nathaniel', 'Mateev', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (959, 'Alberta', 'MacNeachtain', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (960, 'Morry', 'Tomala', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (961, 'Jessy', 'Guido', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (962, 'Lyndel', 'Donalson', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (963, 'King', 'De Winton', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (964, 'Janek', 'Tarrier', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (965, 'Justis', 'Looney', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (966, 'Dennie', 'Petow', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (967, 'Wandis', 'Mounfield', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (968, 'Rollo', 'MacKnockiter', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (969, 'Glyn', 'Brusin', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (970, 'Rutledge', 'Sire', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (971, 'Angelle', 'Willsmore', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (972, 'Timmie', 'Thieme', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (973, 'Sheeree', 'Kenealy', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (974, 'Sofie', 'Fuentes', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (975, 'Rania', 'Thornthwaite', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (976, 'Del', 'Posner', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (977, 'Carrol', 'Cranston', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (978, 'Aldin', 'Douty', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (979, 'Gabby', 'Dalgleish', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (980, 'Emmet', 'Webben', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (981, 'Moses', 'Coltman', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (982, 'Helsa', 'MacCauley', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (983, 'Dickie', 'Sibley', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (984, 'Belva', 'Cogswell', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (985, 'Gare', 'Froud', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (986, 'Marcie', 'Bury', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (987, 'Lilllie', 'Ecles', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (988, 'Auria', 'Lankester', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (989, 'Bernadette', 'Croxall', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (990, 'Rhody', 'Pochet', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (991, 'Katherine', 'Cubbin', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (992, 'Dierdre', 'Schulz', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (993, 'Emili', 'Newbury', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (994, 'Jillie', 'McRae', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (995, 'Maren', 'Quinnelly', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (996, 'Siana', 'Gilbank', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (997, 'Herby', 'Elsworth', 'S');
                insert into store_customer (id, first_name, last_name, membership) values (998, 'Manon', 'McCarlie', 'B');
                insert into store_customer (id, first_name, last_name, membership) values (999, 'Pauly', 'Schanke', 'G');
                insert into store_customer (id, first_name, last_name, membership) values (1000, 'Gareth', 'Hablot', 'G');
            ''',
            '''
                insert into store_order (id, created_at, payment_status, customer_id) values (1, '2023-05-18 19:19:56', 'P', 12);
                insert into store_order (id, created_at, payment_status, customer_id) values (2, '2023-10-23 15:01:47', 'F', 790);
                insert into store_order (id, created_at, payment_status, customer_id) values (3, '2024-03-09 03:28:58', 'F', 644);
                insert into store_order (id, created_at, payment_status, customer_id) values (4, '2022-09-24 03:05:57', 'F', 745);
                insert into store_order (id, created_at, payment_status, customer_id) values (5, '2023-08-13 18:02:24', 'P', 598);
                insert into store_order (id, created_at, payment_status, customer_id) values (6, '2023-01-16 15:53:57', 'C', 879);
                insert into store_order (id, created_at, payment_status, customer_id) values (7, '2024-05-04 12:54:08', 'C', 602);
                insert into store_order (id, created_at, payment_status, customer_id) values (8, '2023-11-21 12:50:00', 'C', 799);
                insert into store_order (id, created_at, payment_status, customer_id) values (9, '2023-10-29 00:05:50', 'P', 390);
                insert into store_order (id, created_at, payment_status, customer_id) values (10, '2023-06-17 05:55:29', 'C', 460);
                insert into store_order (id, created_at, payment_status, customer_id) values (11, '2024-01-22 22:37:12', 'F', 942);
                insert into store_order (id, created_at, payment_status, customer_id) values (12, '2023-08-17 03:42:57', 'P', 972);
                insert into store_order (id, created_at, payment_status, customer_id) values (13, '2023-10-19 16:32:10', 'P', 381);
                insert into store_order (id, created_at, payment_status, customer_id) values (14, '2023-04-03 10:38:55', 'F', 677);
                insert into store_order (id, created_at, payment_status, customer_id) values (15, '2024-07-03 10:40:18', 'P', 817);
                insert into store_order (id, created_at, payment_status, customer_id) values (16, '2024-05-19 15:58:42', 'C', 55);
                insert into store_order (id, created_at, payment_status, customer_id) values (17, '2024-04-03 09:53:10', 'C', 843);
                insert into store_order (id, created_at, payment_status, customer_id) values (18, '2023-05-10 23:05:05', 'F', 967);
                insert into store_order (id, created_at, payment_status, customer_id) values (19, '2023-09-20 02:17:58', 'P', 650);
                insert into store_order (id, created_at, payment_status, customer_id) values (20, '2023-09-24 02:10:39', 'C', 566);
                insert into store_order (id, created_at, payment_status, customer_id) values (21, '2022-12-15 01:48:02', 'F', 915);
                insert into store_order (id, created_at, payment_status, customer_id) values (22, '2023-03-17 19:17:56', 'C', 327);
                insert into store_order (id, created_at, payment_status, customer_id) values (23, '2024-02-11 04:31:28', 'F', 770);
                insert into store_order (id, created_at, payment_status, customer_id) values (24, '2024-04-30 00:30:34', 'C', 886);
                insert into store_order (id, created_at, payment_status, customer_id) values (25, '2022-10-21 21:41:52', 'C', 489);
                insert into store_order (id, created_at, payment_status, customer_id) values (26, '2023-03-03 11:11:33', 'P', 239);
                insert into store_order (id, created_at, payment_status, customer_id) values (27, '2024-02-23 10:58:55', 'P', 105);
                insert into store_order (id, created_at, payment_status, customer_id) values (28, '2022-10-17 01:11:57', 'C', 179);
                insert into store_order (id, created_at, payment_status, customer_id) values (29, '2023-08-14 23:45:30', 'C', 639);
                insert into store_order (id, created_at, payment_status, customer_id) values (30, '2024-01-21 13:57:22', 'C', 439);
                insert into store_order (id, created_at, payment_status, customer_id) values (31, '2024-04-25 18:32:49', 'C', 520);
                insert into store_order (id, created_at, payment_status, customer_id) values (32, '2023-11-10 14:56:16', 'F', 394);
                insert into store_order (id, created_at, payment_status, customer_id) values (33, '2024-04-23 08:01:04', 'P', 494);
                insert into store_order (id, created_at, payment_status, customer_id) values (34, '2024-06-17 10:58:42', 'P', 674);
                insert into store_order (id, created_at, payment_status, customer_id) values (35, '2023-07-17 17:08:31', 'P', 306);
                insert into store_order (id, created_at, payment_status, customer_id) values (36, '2022-11-13 23:49:44', 'F', 767);
                insert into store_order (id, created_at, payment_status, customer_id) values (37, '2022-09-04 12:12:00', 'C', 858);
                insert into store_order (id, created_at, payment_status, customer_id) values (38, '2023-11-13 11:23:33', 'P', 514);
                insert into store_order (id, created_at, payment_status, customer_id) values (39, '2024-04-22 22:39:47', 'P', 858);
                insert into store_order (id, created_at, payment_status, customer_id) values (40, '2022-12-27 07:22:14', 'P', 603);
                insert into store_order (id, created_at, payment_status, customer_id) values (41, '2022-11-23 23:22:37', 'C', 606);
                insert into store_order (id, created_at, payment_status, customer_id) values (42, '2022-11-02 08:23:00', 'P', 877);
                insert into store_order (id, created_at, payment_status, customer_id) values (43, '2022-08-04 20:47:00', 'F', 971);
                insert into store_order (id, created_at, payment_status, customer_id) values (44, '2024-01-22 04:45:01', 'F', 339);
                insert into store_order (id, created_at, payment_status, customer_id) values (45, '2023-10-14 08:47:32', 'F', 434);
                insert into store_order (id, created_at, payment_status, customer_id) values (46, '2024-01-16 16:18:22', 'P', 59);
                insert into store_order (id, created_at, payment_status, customer_id) values (47, '2024-03-02 17:54:28', 'C', 219);
                insert into store_order (id, created_at, payment_status, customer_id) values (48, '2022-07-20 11:24:27', 'P', 919);
                insert into store_order (id, created_at, payment_status, customer_id) values (49, '2024-04-26 21:23:15', 'F', 115);
                insert into store_order (id, created_at, payment_status, customer_id) values (50, '2024-05-25 21:44:46', 'C', 673);
                insert into store_order (id, created_at, payment_status, customer_id) values (51, '2023-06-27 22:57:14', 'F', 537);
                insert into store_order (id, created_at, payment_status, customer_id) values (52, '2023-01-21 23:18:49', 'F', 54);
                insert into store_order (id, created_at, payment_status, customer_id) values (53, '2022-08-19 01:32:13', 'C', 57);
                insert into store_order (id, created_at, payment_status, customer_id) values (54, '2023-07-04 08:25:00', 'F', 296);
                insert into store_order (id, created_at, payment_status, customer_id) values (55, '2022-09-05 16:57:34', 'P', 815);
                insert into store_order (id, created_at, payment_status, customer_id) values (56, '2023-09-18 20:53:02', 'F', 735);
                insert into store_order (id, created_at, payment_status, customer_id) values (57, '2023-07-18 10:41:55', 'P', 756);
                insert into store_order (id, created_at, payment_status, customer_id) values (58, '2024-03-28 09:09:14', 'C', 566);
                insert into store_order (id, created_at, payment_status, customer_id) values (59, '2022-09-04 02:33:09', 'F', 808);
                insert into store_order (id, created_at, payment_status, customer_id) values (60, '2023-12-03 03:04:07', 'P', 169);
                insert into store_order (id, created_at, payment_status, customer_id) values (61, '2023-09-16 17:47:38', 'P', 574);
                insert into store_order (id, created_at, payment_status, customer_id) values (62, '2024-06-14 14:12:36', 'F', 88);
                insert into store_order (id, created_at, payment_status, customer_id) values (63, '2023-12-17 06:22:33', 'C', 872);
                insert into store_order (id, created_at, payment_status, customer_id) values (64, '2024-04-15 08:42:51', 'P', 245);
                insert into store_order (id, created_at, payment_status, customer_id) values (65, '2023-09-11 08:46:06', 'C', 965);
                insert into store_order (id, created_at, payment_status, customer_id) values (66, '2024-05-10 07:45:56', 'C', 239);
                insert into store_order (id, created_at, payment_status, customer_id) values (67, '2023-09-13 07:04:49', 'P', 715);
                insert into store_order (id, created_at, payment_status, customer_id) values (68, '2023-08-02 21:32:49', 'F', 716);
                insert into store_order (id, created_at, payment_status, customer_id) values (69, '2023-01-28 11:11:29', 'F', 391);
                insert into store_order (id, created_at, payment_status, customer_id) values (70, '2023-09-09 22:53:10', 'P', 692);
                insert into store_order (id, created_at, payment_status, customer_id) values (71, '2022-10-22 06:13:17', 'C', 677);
                insert into store_order (id, created_at, payment_status, customer_id) values (72, '2022-09-15 15:25:35', 'C', 298);
                insert into store_order (id, created_at, payment_status, customer_id) values (73, '2024-04-25 12:29:25', 'P', 868);
                insert into store_order (id, created_at, payment_status, customer_id) values (74, '2023-05-17 23:07:21', 'F', 331);
                insert into store_order (id, created_at, payment_status, customer_id) values (75, '2022-11-19 17:43:42', 'C', 44);
                insert into store_order (id, created_at, payment_status, customer_id) values (76, '2022-08-18 10:16:33', 'P', 882);
                insert into store_order (id, created_at, payment_status, customer_id) values (77, '2023-03-01 22:03:25', 'F', 996);
                insert into store_order (id, created_at, payment_status, customer_id) values (78, '2022-08-30 21:54:44', 'C', 853);
                insert into store_order (id, created_at, payment_status, customer_id) values (79, '2023-06-26 17:46:55', 'P', 915);
                insert into store_order (id, created_at, payment_status, customer_id) values (80, '2023-09-22 02:37:16', 'F', 211);
                insert into store_order (id, created_at, payment_status, customer_id) values (81, '2024-01-23 07:51:39', 'F', 629);
                insert into store_order (id, created_at, payment_status, customer_id) values (82, '2023-06-07 05:54:44', 'P', 607);
                insert into store_order (id, created_at, payment_status, customer_id) values (83, '2022-08-04 03:26:34', 'P', 789);
                insert into store_order (id, created_at, payment_status, customer_id) values (84, '2022-12-23 20:08:01', 'P', 208);
                insert into store_order (id, created_at, payment_status, customer_id) values (85, '2023-03-11 00:18:17', 'F', 681);
                insert into store_order (id, created_at, payment_status, customer_id) values (86, '2024-01-07 22:42:15', 'F', 564);
                insert into store_order (id, created_at, payment_status, customer_id) values (87, '2023-01-14 00:45:37', 'P', 942);
                insert into store_order (id, created_at, payment_status, customer_id) values (88, '2023-02-15 12:35:25', 'P', 932);
                insert into store_order (id, created_at, payment_status, customer_id) values (89, '2023-02-11 20:50:39', 'C', 20);
                insert into store_order (id, created_at, payment_status, customer_id) values (90, '2023-12-22 17:04:19', 'P', 159);
                insert into store_order (id, created_at, payment_status, customer_id) values (91, '2023-12-25 10:11:45', 'C', 288);
                insert into store_order (id, created_at, payment_status, customer_id) values (92, '2024-05-31 16:12:11', 'F', 59);
                insert into store_order (id, created_at, payment_status, customer_id) values (93, '2024-03-12 06:19:08', 'F', 627);
                insert into store_order (id, created_at, payment_status, customer_id) values (94, '2022-12-24 04:00:45', 'C', 585);
                insert into store_order (id, created_at, payment_status, customer_id) values (95, '2023-08-12 16:28:44', 'F', 373);
                insert into store_order (id, created_at, payment_status, customer_id) values (96, '2024-06-30 16:38:21', 'F', 349);
                insert into store_order (id, created_at, payment_status, customer_id) values (97, '2024-02-21 02:09:51', 'C', 805);
                insert into store_order (id, created_at, payment_status, customer_id) values (98, '2023-03-16 18:44:36', 'P', 406);
                insert into store_order (id, created_at, payment_status, customer_id) values (99, '2023-05-09 05:27:55', 'C', 821);
                insert into store_order (id, created_at, payment_status, customer_id) values (100, '2024-02-20 05:48:54', 'P', 242);
                insert into store_order (id, created_at, payment_status, customer_id) values (101, '2023-02-27 02:33:56', 'P', 69);
                insert into store_order (id, created_at, payment_status, customer_id) values (102, '2023-09-26 18:14:33', 'F', 120);
                insert into store_order (id, created_at, payment_status, customer_id) values (103, '2024-04-02 17:10:18', 'C', 166);
                insert into store_order (id, created_at, payment_status, customer_id) values (104, '2024-05-25 10:12:35', 'F', 762);
                insert into store_order (id, created_at, payment_status, customer_id) values (105, '2022-11-21 07:26:14', 'C', 351);
                insert into store_order (id, created_at, payment_status, customer_id) values (106, '2023-05-30 01:06:47', 'P', 890);
                insert into store_order (id, created_at, payment_status, customer_id) values (107, '2022-07-20 15:46:59', 'F', 448);
                insert into store_order (id, created_at, payment_status, customer_id) values (108, '2024-01-12 16:38:28', 'F', 53);
                insert into store_order (id, created_at, payment_status, customer_id) values (109, '2024-02-04 13:22:59', 'C', 449);
                insert into store_order (id, created_at, payment_status, customer_id) values (110, '2023-12-18 21:11:37', 'C', 362);
                insert into store_order (id, created_at, payment_status, customer_id) values (111, '2024-04-25 21:45:09', 'C', 776);
                insert into store_order (id, created_at, payment_status, customer_id) values (112, '2024-03-12 11:10:39', 'F', 40);
                insert into store_order (id, created_at, payment_status, customer_id) values (113, '2023-08-12 00:48:11', 'C', 613);
                insert into store_order (id, created_at, payment_status, customer_id) values (114, '2022-11-20 12:48:12', 'C', 504);
                insert into store_order (id, created_at, payment_status, customer_id) values (115, '2024-05-20 15:30:40', 'F', 655);
                insert into store_order (id, created_at, payment_status, customer_id) values (116, '2024-06-19 18:12:51', 'F', 332);
                insert into store_order (id, created_at, payment_status, customer_id) values (117, '2024-06-21 06:29:44', 'P', 675);
                insert into store_order (id, created_at, payment_status, customer_id) values (118, '2022-11-27 13:03:46', 'C', 828);
                insert into store_order (id, created_at, payment_status, customer_id) values (119, '2023-07-27 08:50:17', 'P', 159);
                insert into store_order (id, created_at, payment_status, customer_id) values (120, '2022-07-24 16:25:34', 'P', 886);
                insert into store_order (id, created_at, payment_status, customer_id) values (121, '2023-05-09 19:13:01', 'F', 628);
                insert into store_order (id, created_at, payment_status, customer_id) values (122, '2023-12-28 01:19:17', 'F', 981);
                insert into store_order (id, created_at, payment_status, customer_id) values (123, '2023-06-28 01:34:41', 'P', 68);
                insert into store_order (id, created_at, payment_status, customer_id) values (124, '2024-04-02 04:02:11', 'C', 970);
                insert into store_order (id, created_at, payment_status, customer_id) values (125, '2022-10-30 18:30:49', 'F', 628);
                insert into store_order (id, created_at, payment_status, customer_id) values (126, '2023-02-02 21:56:27', 'C', 460);
                insert into store_order (id, created_at, payment_status, customer_id) values (127, '2023-05-26 14:22:51', 'P', 363);
                insert into store_order (id, created_at, payment_status, customer_id) values (128, '2024-06-10 20:55:37', 'P', 322);
                insert into store_order (id, created_at, payment_status, customer_id) values (129, '2023-04-14 02:28:34', 'F', 957);
                insert into store_order (id, created_at, payment_status, customer_id) values (130, '2023-08-31 16:06:30', 'F', 484);
                insert into store_order (id, created_at, payment_status, customer_id) values (131, '2022-10-12 01:02:07', 'P', 690);
                insert into store_order (id, created_at, payment_status, customer_id) values (132, '2024-02-29 05:59:08', 'C', 667);
                insert into store_order (id, created_at, payment_status, customer_id) values (133, '2022-09-14 10:29:16', 'C', 366);
                insert into store_order (id, created_at, payment_status, customer_id) values (134, '2022-11-13 13:29:32', 'P', 660);
                insert into store_order (id, created_at, payment_status, customer_id) values (135, '2023-06-21 10:56:06', 'F', 103);
                insert into store_order (id, created_at, payment_status, customer_id) values (136, '2023-06-15 11:27:34', 'C', 88);
                insert into store_order (id, created_at, payment_status, customer_id) values (137, '2022-08-28 02:50:58', 'F', 581);
                insert into store_order (id, created_at, payment_status, customer_id) values (138, '2024-05-17 23:13:29', 'F', 863);
                insert into store_order (id, created_at, payment_status, customer_id) values (139, '2022-10-14 08:16:47', 'P', 536);
                insert into store_order (id, created_at, payment_status, customer_id) values (140, '2022-08-22 00:20:40', 'F', 980);
                insert into store_order (id, created_at, payment_status, customer_id) values (141, '2024-02-07 18:37:28', 'C', 812);
                insert into store_order (id, created_at, payment_status, customer_id) values (142, '2024-05-21 04:58:30', 'F', 507);
                insert into store_order (id, created_at, payment_status, customer_id) values (143, '2023-10-03 03:45:17', 'P', 763);
                insert into store_order (id, created_at, payment_status, customer_id) values (144, '2022-07-13 05:53:37', 'P', 897);
                insert into store_order (id, created_at, payment_status, customer_id) values (145, '2024-05-05 05:49:47', 'C', 221);
                insert into store_order (id, created_at, payment_status, customer_id) values (146, '2024-02-24 20:24:14', 'F', 31);
                insert into store_order (id, created_at, payment_status, customer_id) values (147, '2022-07-15 00:37:35', 'P', 260);
                insert into store_order (id, created_at, payment_status, customer_id) values (148, '2023-11-05 04:19:12', 'P', 948);
                insert into store_order (id, created_at, payment_status, customer_id) values (149, '2024-01-05 20:52:29', 'F', 841);
                insert into store_order (id, created_at, payment_status, customer_id) values (150, '2023-09-20 06:34:10', 'F', 194);
                insert into store_order (id, created_at, payment_status, customer_id) values (151, '2023-09-22 10:32:17', 'F', 394);
                insert into store_order (id, created_at, payment_status, customer_id) values (152, '2023-12-25 00:07:23', 'F', 356);
                insert into store_order (id, created_at, payment_status, customer_id) values (153, '2024-05-20 10:43:43', 'P', 342);
                insert into store_order (id, created_at, payment_status, customer_id) values (154, '2023-09-14 00:54:00', 'C', 81);
                insert into store_order (id, created_at, payment_status, customer_id) values (155, '2023-10-17 16:52:33', 'P', 731);
                insert into store_order (id, created_at, payment_status, customer_id) values (156, '2022-10-06 08:36:21', 'C', 984);
                insert into store_order (id, created_at, payment_status, customer_id) values (157, '2022-07-08 22:36:29', 'P', 608);
                insert into store_order (id, created_at, payment_status, customer_id) values (158, '2024-03-22 15:01:30', 'C', 897);
                insert into store_order (id, created_at, payment_status, customer_id) values (159, '2024-04-28 06:36:31', 'C', 800);
                insert into store_order (id, created_at, payment_status, customer_id) values (160, '2023-03-25 15:30:29', 'C', 855);
                insert into store_order (id, created_at, payment_status, customer_id) values (161, '2022-11-10 14:28:28', 'F', 906);
                insert into store_order (id, created_at, payment_status, customer_id) values (162, '2023-04-10 03:45:53', 'F', 649);
                insert into store_order (id, created_at, payment_status, customer_id) values (163, '2023-08-25 09:26:35', 'F', 610);
                insert into store_order (id, created_at, payment_status, customer_id) values (164, '2023-01-19 08:20:00', 'F', 482);
                insert into store_order (id, created_at, payment_status, customer_id) values (165, '2024-03-19 20:23:02', 'F', 110);
                insert into store_order (id, created_at, payment_status, customer_id) values (166, '2023-12-28 09:09:12', 'F', 636);
                insert into store_order (id, created_at, payment_status, customer_id) values (167, '2022-11-06 18:03:05', 'C', 322);
                insert into store_order (id, created_at, payment_status, customer_id) values (168, '2023-10-14 13:23:24', 'F', 199);
                insert into store_order (id, created_at, payment_status, customer_id) values (169, '2023-12-27 15:12:38', 'F', 999);
                insert into store_order (id, created_at, payment_status, customer_id) values (170, '2024-05-11 05:33:54', 'C', 803);
                insert into store_order (id, created_at, payment_status, customer_id) values (171, '2023-06-17 03:51:12', 'F', 98);
                insert into store_order (id, created_at, payment_status, customer_id) values (172, '2023-08-30 22:24:18', 'P', 983);
                insert into store_order (id, created_at, payment_status, customer_id) values (173, '2023-06-16 06:54:05', 'P', 707);
                insert into store_order (id, created_at, payment_status, customer_id) values (174, '2023-11-12 06:53:30', 'P', 144);
                insert into store_order (id, created_at, payment_status, customer_id) values (175, '2024-04-04 13:07:42', 'P', 122);
                insert into store_order (id, created_at, payment_status, customer_id) values (176, '2024-02-15 21:02:08', 'C', 311);
                insert into store_order (id, created_at, payment_status, customer_id) values (177, '2022-07-19 02:53:25', 'P', 134);
                insert into store_order (id, created_at, payment_status, customer_id) values (178, '2023-02-22 11:34:44', 'C', 49);
                insert into store_order (id, created_at, payment_status, customer_id) values (179, '2023-09-19 18:45:38', 'C', 65);
                insert into store_order (id, created_at, payment_status, customer_id) values (180, '2024-02-05 16:32:52', 'F', 587);
                insert into store_order (id, created_at, payment_status, customer_id) values (181, '2023-01-16 23:34:24', 'P', 157);
                insert into store_order (id, created_at, payment_status, customer_id) values (182, '2022-12-10 19:53:15', 'P', 38);
                insert into store_order (id, created_at, payment_status, customer_id) values (183, '2024-02-05 15:21:55', 'P', 486);
                insert into store_order (id, created_at, payment_status, customer_id) values (184, '2024-02-16 20:51:23', 'P', 965);
                insert into store_order (id, created_at, payment_status, customer_id) values (185, '2022-08-17 08:13:02', 'P', 253);
                insert into store_order (id, created_at, payment_status, customer_id) values (186, '2022-07-13 23:26:19', 'P', 635);
                insert into store_order (id, created_at, payment_status, customer_id) values (187, '2022-12-08 22:40:07', 'C', 584);
                insert into store_order (id, created_at, payment_status, customer_id) values (188, '2023-07-31 21:09:59', 'F', 595);
                insert into store_order (id, created_at, payment_status, customer_id) values (189, '2022-11-03 14:37:00', 'C', 311);
                insert into store_order (id, created_at, payment_status, customer_id) values (190, '2024-05-23 20:32:25', 'P', 359);
                insert into store_order (id, created_at, payment_status, customer_id) values (191, '2023-03-27 07:14:33', 'F', 173);
                insert into store_order (id, created_at, payment_status, customer_id) values (192, '2022-09-19 07:12:02', 'P', 135);
                insert into store_order (id, created_at, payment_status, customer_id) values (193, '2023-05-02 00:05:41', 'C', 894);
                insert into store_order (id, created_at, payment_status, customer_id) values (194, '2022-07-18 14:45:46', 'C', 851);
                insert into store_order (id, created_at, payment_status, customer_id) values (195, '2022-11-10 06:17:22', 'F', 12);
                insert into store_order (id, created_at, payment_status, customer_id) values (196, '2023-01-17 21:20:24', 'C', 595);
                insert into store_order (id, created_at, payment_status, customer_id) values (197, '2023-05-11 22:09:47', 'C', 196);
                insert into store_order (id, created_at, payment_status, customer_id) values (198, '2023-03-02 18:15:54', 'P', 799);
                insert into store_order (id, created_at, payment_status, customer_id) values (199, '2022-10-20 02:24:20', 'F', 70);
                insert into store_order (id, created_at, payment_status, customer_id) values (200, '2022-10-30 05:59:11', 'F', 407);
                insert into store_order (id, created_at, payment_status, customer_id) values (201, '2024-03-22 00:59:39', 'P', 743);
                insert into store_order (id, created_at, payment_status, customer_id) values (202, '2024-02-14 10:20:40', 'P', 417);
                insert into store_order (id, created_at, payment_status, customer_id) values (203, '2024-02-09 14:27:36', 'F', 572);
                insert into store_order (id, created_at, payment_status, customer_id) values (204, '2024-04-03 06:49:10', 'F', 147);
                insert into store_order (id, created_at, payment_status, customer_id) values (205, '2024-06-11 01:31:47', 'P', 826);
                insert into store_order (id, created_at, payment_status, customer_id) values (206, '2023-03-23 03:18:51', 'F', 242);
                insert into store_order (id, created_at, payment_status, customer_id) values (207, '2023-12-09 03:35:46', 'F', 109);
                insert into store_order (id, created_at, payment_status, customer_id) values (208, '2024-02-06 05:58:12', 'C', 182);
                insert into store_order (id, created_at, payment_status, customer_id) values (209, '2023-07-30 16:01:28', 'C', 269);
                insert into store_order (id, created_at, payment_status, customer_id) values (210, '2023-06-11 08:01:11', 'F', 621);
                insert into store_order (id, created_at, payment_status, customer_id) values (211, '2024-01-09 12:15:40', 'F', 412);
                insert into store_order (id, created_at, payment_status, customer_id) values (212, '2023-09-13 04:41:20', 'C', 779);
                insert into store_order (id, created_at, payment_status, customer_id) values (213, '2022-11-30 01:15:08', 'P', 281);
                insert into store_order (id, created_at, payment_status, customer_id) values (214, '2024-06-28 16:44:45', 'P', 851);
                insert into store_order (id, created_at, payment_status, customer_id) values (215, '2022-10-22 01:45:21', 'F', 866);
                insert into store_order (id, created_at, payment_status, customer_id) values (216, '2024-05-13 12:08:43', 'F', 156);
                insert into store_order (id, created_at, payment_status, customer_id) values (217, '2023-01-16 02:32:51', 'F', 638);
                insert into store_order (id, created_at, payment_status, customer_id) values (218, '2023-07-30 03:32:14', 'C', 715);
                insert into store_order (id, created_at, payment_status, customer_id) values (219, '2023-08-19 20:53:56', 'P', 581);
                insert into store_order (id, created_at, payment_status, customer_id) values (220, '2023-08-26 02:15:31', 'C', 795);
                insert into store_order (id, created_at, payment_status, customer_id) values (221, '2024-05-29 11:20:04', 'C', 228);
                insert into store_order (id, created_at, payment_status, customer_id) values (222, '2023-03-01 21:11:28', 'P', 248);
                insert into store_order (id, created_at, payment_status, customer_id) values (223, '2023-11-27 05:28:11', 'P', 994);
                insert into store_order (id, created_at, payment_status, customer_id) values (224, '2022-08-07 02:57:40', 'P', 185);
                insert into store_order (id, created_at, payment_status, customer_id) values (225, '2023-01-16 01:25:50', 'P', 335);
                insert into store_order (id, created_at, payment_status, customer_id) values (226, '2024-05-04 02:15:39', 'P', 219);
                insert into store_order (id, created_at, payment_status, customer_id) values (227, '2023-03-04 21:51:32', 'F', 617);
                insert into store_order (id, created_at, payment_status, customer_id) values (228, '2022-11-16 18:43:49', 'C', 814);
                insert into store_order (id, created_at, payment_status, customer_id) values (229, '2023-07-04 12:57:08', 'P', 291);
                insert into store_order (id, created_at, payment_status, customer_id) values (230, '2024-01-03 20:29:25', 'P', 360);
                insert into store_order (id, created_at, payment_status, customer_id) values (231, '2022-11-17 07:39:14', 'P', 815);
                insert into store_order (id, created_at, payment_status, customer_id) values (232, '2024-04-02 09:19:58', 'C', 284);
                insert into store_order (id, created_at, payment_status, customer_id) values (233, '2023-10-05 19:53:55', 'C', 865);
                insert into store_order (id, created_at, payment_status, customer_id) values (234, '2024-04-19 12:42:41', 'P', 746);
                insert into store_order (id, created_at, payment_status, customer_id) values (235, '2023-06-17 23:15:28', 'P', 536);
                insert into store_order (id, created_at, payment_status, customer_id) values (236, '2022-08-16 21:17:54', 'P', 436);
                insert into store_order (id, created_at, payment_status, customer_id) values (237, '2022-10-08 11:37:09', 'P', 912);
                insert into store_order (id, created_at, payment_status, customer_id) values (238, '2023-01-25 17:11:38', 'F', 33);
                insert into store_order (id, created_at, payment_status, customer_id) values (239, '2023-05-12 16:25:54', 'F', 654);
                insert into store_order (id, created_at, payment_status, customer_id) values (240, '2023-08-19 18:42:37', 'P', 766);
                insert into store_order (id, created_at, payment_status, customer_id) values (241, '2023-02-22 08:47:17', 'C', 159);
                insert into store_order (id, created_at, payment_status, customer_id) values (242, '2023-09-20 09:35:47', 'C', 577);
                insert into store_order (id, created_at, payment_status, customer_id) values (243, '2022-07-26 12:17:48', 'F', 662);
                insert into store_order (id, created_at, payment_status, customer_id) values (244, '2023-01-19 21:08:02', 'F', 208);
                insert into store_order (id, created_at, payment_status, customer_id) values (245, '2022-12-03 03:56:34', 'P', 837);
                insert into store_order (id, created_at, payment_status, customer_id) values (246, '2023-12-02 18:39:30', 'C', 526);
                insert into store_order (id, created_at, payment_status, customer_id) values (247, '2023-02-26 18:19:54', 'C', 573);
                insert into store_order (id, created_at, payment_status, customer_id) values (248, '2024-01-13 17:56:55', 'F', 646);
                insert into store_order (id, created_at, payment_status, customer_id) values (249, '2023-07-25 17:27:33', 'F', 233);
                insert into store_order (id, created_at, payment_status, customer_id) values (250, '2023-11-28 07:47:44', 'C', 859);
                insert into store_order (id, created_at, payment_status, customer_id) values (251, '2023-11-20 12:43:03', 'P', 904);
                insert into store_order (id, created_at, payment_status, customer_id) values (252, '2022-10-21 06:50:22', 'P', 682);
                insert into store_order (id, created_at, payment_status, customer_id) values (253, '2023-02-14 12:00:13', 'F', 513);
                insert into store_order (id, created_at, payment_status, customer_id) values (254, '2022-11-02 04:42:59', 'P', 482);
                insert into store_order (id, created_at, payment_status, customer_id) values (255, '2023-01-07 14:29:23', 'F', 765);
                insert into store_order (id, created_at, payment_status, customer_id) values (256, '2024-03-20 11:25:29', 'C', 423);
                insert into store_order (id, created_at, payment_status, customer_id) values (257, '2022-09-14 14:23:10', 'P', 826);
                insert into store_order (id, created_at, payment_status, customer_id) values (258, '2023-04-06 23:51:27', 'P', 257);
                insert into store_order (id, created_at, payment_status, customer_id) values (259, '2023-08-07 15:19:13', 'P', 606);
                insert into store_order (id, created_at, payment_status, customer_id) values (260, '2022-09-05 01:04:23', 'C', 66);
                insert into store_order (id, created_at, payment_status, customer_id) values (261, '2024-03-21 16:13:33', 'F', 903);
                insert into store_order (id, created_at, payment_status, customer_id) values (262, '2023-02-02 13:19:59', 'P', 368);
                insert into store_order (id, created_at, payment_status, customer_id) values (263, '2022-07-31 22:41:02', 'P', 566);
                insert into store_order (id, created_at, payment_status, customer_id) values (264, '2024-04-28 01:18:50', 'C', 592);
                insert into store_order (id, created_at, payment_status, customer_id) values (265, '2024-04-05 10:31:38', 'P', 577);
                insert into store_order (id, created_at, payment_status, customer_id) values (266, '2024-03-24 06:24:52', 'P', 325);
                insert into store_order (id, created_at, payment_status, customer_id) values (267, '2023-08-22 08:29:46', 'C', 386);
                insert into store_order (id, created_at, payment_status, customer_id) values (268, '2023-10-03 07:38:55', 'C', 118);
                insert into store_order (id, created_at, payment_status, customer_id) values (269, '2023-11-27 05:03:07', 'F', 656);
                insert into store_order (id, created_at, payment_status, customer_id) values (270, '2023-02-22 21:14:12', 'C', 875);
                insert into store_order (id, created_at, payment_status, customer_id) values (271, '2022-11-16 19:56:50', 'P', 682);
                insert into store_order (id, created_at, payment_status, customer_id) values (272, '2023-11-02 10:49:43', 'C', 725);
                insert into store_order (id, created_at, payment_status, customer_id) values (273, '2023-12-08 07:46:32', 'C', 350);
                insert into store_order (id, created_at, payment_status, customer_id) values (274, '2022-10-21 17:17:09', 'P', 116);
                insert into store_order (id, created_at, payment_status, customer_id) values (275, '2024-01-14 01:30:20', 'P', 309);
                insert into store_order (id, created_at, payment_status, customer_id) values (276, '2023-12-07 15:10:02', 'F', 397);
                insert into store_order (id, created_at, payment_status, customer_id) values (277, '2023-11-07 12:04:46', 'P', 593);
                insert into store_order (id, created_at, payment_status, customer_id) values (278, '2022-12-24 21:12:38', 'C', 442);
                insert into store_order (id, created_at, payment_status, customer_id) values (279, '2022-11-21 21:22:42', 'F', 989);
                insert into store_order (id, created_at, payment_status, customer_id) values (280, '2023-07-05 21:46:59', 'F', 794);
                insert into store_order (id, created_at, payment_status, customer_id) values (281, '2022-11-30 15:46:38', 'P', 729);
                insert into store_order (id, created_at, payment_status, customer_id) values (282, '2023-11-06 22:20:31', 'F', 878);
                insert into store_order (id, created_at, payment_status, customer_id) values (283, '2023-12-09 01:38:47', 'F', 332);
                insert into store_order (id, created_at, payment_status, customer_id) values (284, '2022-07-10 15:15:10', 'P', 511);
                insert into store_order (id, created_at, payment_status, customer_id) values (285, '2023-03-19 02:07:48', 'C', 45);
                insert into store_order (id, created_at, payment_status, customer_id) values (286, '2023-04-28 00:41:03', 'P', 379);
                insert into store_order (id, created_at, payment_status, customer_id) values (287, '2023-01-06 05:07:53', 'F', 870);
                insert into store_order (id, created_at, payment_status, customer_id) values (288, '2023-10-25 01:18:02', 'C', 270);
                insert into store_order (id, created_at, payment_status, customer_id) values (289, '2023-07-25 21:37:48', 'C', 612);
                insert into store_order (id, created_at, payment_status, customer_id) values (290, '2022-10-15 05:34:32', 'P', 932);
                insert into store_order (id, created_at, payment_status, customer_id) values (291, '2024-04-27 03:24:49', 'C', 549);
                insert into store_order (id, created_at, payment_status, customer_id) values (292, '2024-06-12 16:37:12', 'C', 236);
                insert into store_order (id, created_at, payment_status, customer_id) values (293, '2022-07-15 16:11:07', 'F', 958);
                insert into store_order (id, created_at, payment_status, customer_id) values (294, '2023-07-24 09:53:13', 'P', 169);
                insert into store_order (id, created_at, payment_status, customer_id) values (295, '2024-06-29 05:52:48', 'F', 630);
                insert into store_order (id, created_at, payment_status, customer_id) values (296, '2023-12-23 21:22:25', 'P', 821);
                insert into store_order (id, created_at, payment_status, customer_id) values (297, '2022-08-29 16:03:35', 'C', 380);
                insert into store_order (id, created_at, payment_status, customer_id) values (298, '2022-08-11 16:36:49', 'P', 359);
                insert into store_order (id, created_at, payment_status, customer_id) values (299, '2022-07-15 22:28:44', 'C', 362);
                insert into store_order (id, created_at, payment_status, customer_id) values (300, '2022-11-29 20:13:27', 'P', 714);
                insert into store_order (id, created_at, payment_status, customer_id) values (301, '2023-03-07 14:59:33', 'P', 441);
                insert into store_order (id, created_at, payment_status, customer_id) values (302, '2024-05-12 12:57:10', 'P', 793);
                insert into store_order (id, created_at, payment_status, customer_id) values (303, '2023-09-05 20:06:21', 'P', 440);
                insert into store_order (id, created_at, payment_status, customer_id) values (304, '2023-02-19 06:28:28', 'C', 51);
                insert into store_order (id, created_at, payment_status, customer_id) values (305, '2023-09-15 00:04:04', 'P', 663);
                insert into store_order (id, created_at, payment_status, customer_id) values (306, '2023-12-24 21:36:20', 'F', 932);
                insert into store_order (id, created_at, payment_status, customer_id) values (307, '2023-03-30 21:24:39', 'P', 780);
                insert into store_order (id, created_at, payment_status, customer_id) values (308, '2022-10-21 13:18:52', 'F', 428);
                insert into store_order (id, created_at, payment_status, customer_id) values (309, '2023-10-21 15:56:36', 'P', 177);
                insert into store_order (id, created_at, payment_status, customer_id) values (310, '2022-07-09 11:19:02', 'F', 741);
                insert into store_order (id, created_at, payment_status, customer_id) values (311, '2023-07-06 13:39:59', 'F', 887);
                insert into store_order (id, created_at, payment_status, customer_id) values (312, '2024-01-16 01:47:41', 'P', 697);
                insert into store_order (id, created_at, payment_status, customer_id) values (313, '2022-09-24 15:30:51', 'F', 343);
                insert into store_order (id, created_at, payment_status, customer_id) values (314, '2023-10-23 13:22:48', 'C', 957);
                insert into store_order (id, created_at, payment_status, customer_id) values (315, '2023-03-28 03:13:13', 'C', 135);
                insert into store_order (id, created_at, payment_status, customer_id) values (316, '2023-10-22 21:04:22', 'F', 947);
                insert into store_order (id, created_at, payment_status, customer_id) values (317, '2024-05-20 11:24:48', 'C', 940);
                insert into store_order (id, created_at, payment_status, customer_id) values (318, '2022-10-26 04:36:19', 'C', 677);
                insert into store_order (id, created_at, payment_status, customer_id) values (319, '2024-02-10 00:19:21', 'C', 580);
                insert into store_order (id, created_at, payment_status, customer_id) values (320, '2024-05-11 21:12:27', 'F', 384);
                insert into store_order (id, created_at, payment_status, customer_id) values (321, '2023-12-06 13:19:14', 'F', 586);
                insert into store_order (id, created_at, payment_status, customer_id) values (322, '2024-02-24 14:09:36', 'F', 416);
                insert into store_order (id, created_at, payment_status, customer_id) values (323, '2023-09-13 13:13:10', 'C', 127);
                insert into store_order (id, created_at, payment_status, customer_id) values (324, '2023-12-14 02:53:50', 'F', 568);
                insert into store_order (id, created_at, payment_status, customer_id) values (325, '2023-12-17 01:49:03', 'C', 35);
                insert into store_order (id, created_at, payment_status, customer_id) values (326, '2023-03-07 04:37:38', 'P', 44);
                insert into store_order (id, created_at, payment_status, customer_id) values (327, '2022-08-08 23:57:14', 'C', 526);
                insert into store_order (id, created_at, payment_status, customer_id) values (328, '2022-08-24 20:41:53', 'C', 299);
                insert into store_order (id, created_at, payment_status, customer_id) values (329, '2023-09-06 12:59:46', 'F', 207);
                insert into store_order (id, created_at, payment_status, customer_id) values (330, '2023-06-17 10:11:13', 'F', 440);
                insert into store_order (id, created_at, payment_status, customer_id) values (331, '2023-06-27 07:03:24', 'C', 627);
                insert into store_order (id, created_at, payment_status, customer_id) values (332, '2022-09-27 09:45:00', 'P', 76);
                insert into store_order (id, created_at, payment_status, customer_id) values (333, '2023-04-21 10:00:12', 'F', 749);
                insert into store_order (id, created_at, payment_status, customer_id) values (334, '2022-10-31 21:12:21', 'F', 139);
                insert into store_order (id, created_at, payment_status, customer_id) values (335, '2023-06-01 05:35:10', 'P', 138);
                insert into store_order (id, created_at, payment_status, customer_id) values (336, '2023-04-15 04:02:34', 'F', 667);
                insert into store_order (id, created_at, payment_status, customer_id) values (337, '2023-08-20 17:43:52', 'C', 142);
                insert into store_order (id, created_at, payment_status, customer_id) values (338, '2023-10-27 07:18:34', 'C', 202);
                insert into store_order (id, created_at, payment_status, customer_id) values (339, '2023-10-14 21:32:53', 'P', 623);
                insert into store_order (id, created_at, payment_status, customer_id) values (340, '2024-01-18 04:30:08', 'F', 652);
                insert into store_order (id, created_at, payment_status, customer_id) values (341, '2023-06-12 21:15:05', 'F', 704);
                insert into store_order (id, created_at, payment_status, customer_id) values (342, '2024-04-04 13:25:18', 'P', 648);
                insert into store_order (id, created_at, payment_status, customer_id) values (343, '2023-01-08 05:21:12', 'C', 494);
                insert into store_order (id, created_at, payment_status, customer_id) values (344, '2022-11-21 04:41:15', 'F', 519);
                insert into store_order (id, created_at, payment_status, customer_id) values (345, '2023-10-13 17:13:10', 'F', 801);
                insert into store_order (id, created_at, payment_status, customer_id) values (346, '2024-01-30 02:13:23', 'C', 498);
                insert into store_order (id, created_at, payment_status, customer_id) values (347, '2022-11-04 03:20:49', 'F', 701);
                insert into store_order (id, created_at, payment_status, customer_id) values (348, '2024-07-01 19:28:24', 'C', 163);
                insert into store_order (id, created_at, payment_status, customer_id) values (349, '2023-11-14 21:38:56', 'C', 100);
                insert into store_order (id, created_at, payment_status, customer_id) values (350, '2023-07-16 12:20:08', 'C', 311);
                insert into store_order (id, created_at, payment_status, customer_id) values (351, '2023-10-09 09:47:54', 'P', 260);
                insert into store_order (id, created_at, payment_status, customer_id) values (352, '2024-05-29 01:23:53', 'C', 21);
                insert into store_order (id, created_at, payment_status, customer_id) values (353, '2024-03-16 11:02:05', 'F', 261);
                insert into store_order (id, created_at, payment_status, customer_id) values (354, '2023-08-07 10:56:32', 'C', 912);
                insert into store_order (id, created_at, payment_status, customer_id) values (355, '2022-07-22 04:54:54', 'P', 771);
                insert into store_order (id, created_at, payment_status, customer_id) values (356, '2022-11-18 20:54:59', 'P', 123);
                insert into store_order (id, created_at, payment_status, customer_id) values (357, '2024-03-29 08:40:04', 'F', 44);
                insert into store_order (id, created_at, payment_status, customer_id) values (358, '2023-08-13 04:49:05', 'F', 627);
                insert into store_order (id, created_at, payment_status, customer_id) values (359, '2023-11-14 14:20:06', 'F', 798);
                insert into store_order (id, created_at, payment_status, customer_id) values (360, '2023-04-02 18:10:15', 'P', 295);
                insert into store_order (id, created_at, payment_status, customer_id) values (361, '2022-12-23 13:38:30', 'F', 701);
                insert into store_order (id, created_at, payment_status, customer_id) values (362, '2024-03-19 13:31:21', 'P', 424);
                insert into store_order (id, created_at, payment_status, customer_id) values (363, '2023-11-10 04:28:33', 'C', 296);
                insert into store_order (id, created_at, payment_status, customer_id) values (364, '2022-09-18 07:29:56', 'F', 157);
                insert into store_order (id, created_at, payment_status, customer_id) values (365, '2024-04-18 08:50:51', 'P', 116);
                insert into store_order (id, created_at, payment_status, customer_id) values (366, '2022-12-18 01:51:51', 'F', 797);
                insert into store_order (id, created_at, payment_status, customer_id) values (367, '2022-11-06 13:52:26', 'C', 478);
                insert into store_order (id, created_at, payment_status, customer_id) values (368, '2023-11-09 03:49:00', 'P', 187);
                insert into store_order (id, created_at, payment_status, customer_id) values (369, '2023-05-03 19:04:44', 'P', 113);
                insert into store_order (id, created_at, payment_status, customer_id) values (370, '2022-12-18 08:33:20', 'P', 365);
                insert into store_order (id, created_at, payment_status, customer_id) values (371, '2024-03-31 19:18:26', 'C', 716);
                insert into store_order (id, created_at, payment_status, customer_id) values (372, '2023-01-28 21:12:03', 'C', 640);
                insert into store_order (id, created_at, payment_status, customer_id) values (373, '2023-02-19 19:48:01', 'C', 54);
                insert into store_order (id, created_at, payment_status, customer_id) values (374, '2023-03-30 00:06:48', 'F', 302);
                insert into store_order (id, created_at, payment_status, customer_id) values (375, '2022-08-09 00:18:46', 'C', 847);
                insert into store_order (id, created_at, payment_status, customer_id) values (376, '2023-12-02 18:46:35', 'F', 881);
                insert into store_order (id, created_at, payment_status, customer_id) values (377, '2022-07-21 13:06:02', 'F', 662);
                insert into store_order (id, created_at, payment_status, customer_id) values (378, '2024-05-30 08:13:11', 'C', 710);
                insert into store_order (id, created_at, payment_status, customer_id) values (379, '2022-08-18 01:04:46', 'F', 257);
                insert into store_order (id, created_at, payment_status, customer_id) values (380, '2023-06-17 05:48:08', 'F', 975);
                insert into store_order (id, created_at, payment_status, customer_id) values (381, '2022-10-01 01:08:30', 'C', 151);
                insert into store_order (id, created_at, payment_status, customer_id) values (382, '2024-02-17 14:06:03', 'F', 450);
                insert into store_order (id, created_at, payment_status, customer_id) values (383, '2023-05-08 07:04:57', 'C', 945);
                insert into store_order (id, created_at, payment_status, customer_id) values (384, '2022-09-19 20:13:46', 'F', 888);
                insert into store_order (id, created_at, payment_status, customer_id) values (385, '2022-09-22 04:09:45', 'P', 814);
                insert into store_order (id, created_at, payment_status, customer_id) values (386, '2023-03-21 23:05:36', 'P', 399);
                insert into store_order (id, created_at, payment_status, customer_id) values (387, '2022-08-23 13:59:41', 'P', 714);
                insert into store_order (id, created_at, payment_status, customer_id) values (388, '2023-11-10 20:03:52', 'P', 740);
                insert into store_order (id, created_at, payment_status, customer_id) values (389, '2024-03-29 19:06:12', 'P', 588);
                insert into store_order (id, created_at, payment_status, customer_id) values (390, '2023-07-20 12:40:20', 'F', 336);
                insert into store_order (id, created_at, payment_status, customer_id) values (391, '2022-07-11 23:32:44', 'C', 349);
                insert into store_order (id, created_at, payment_status, customer_id) values (392, '2023-09-19 06:38:36', 'C', 537);
                insert into store_order (id, created_at, payment_status, customer_id) values (393, '2023-12-28 03:15:15', 'F', 36);
                insert into store_order (id, created_at, payment_status, customer_id) values (394, '2023-12-29 00:01:36', 'F', 835);
                insert into store_order (id, created_at, payment_status, customer_id) values (395, '2022-07-09 22:26:16', 'F', 515);
                insert into store_order (id, created_at, payment_status, customer_id) values (396, '2023-02-18 13:38:37', 'P', 509);
                insert into store_order (id, created_at, payment_status, customer_id) values (397, '2022-09-05 22:15:32', 'C', 332);
                insert into store_order (id, created_at, payment_status, customer_id) values (398, '2024-06-06 16:24:32', 'F', 263);
                insert into store_order (id, created_at, payment_status, customer_id) values (399, '2024-04-05 12:34:08', 'C', 500);
                insert into store_order (id, created_at, payment_status, customer_id) values (400, '2023-12-08 00:26:12', 'C', 80);
                insert into store_order (id, created_at, payment_status, customer_id) values (401, '2024-06-07 08:17:35', 'P', 609);
                insert into store_order (id, created_at, payment_status, customer_id) values (402, '2023-10-07 01:57:35', 'P', 213);
                insert into store_order (id, created_at, payment_status, customer_id) values (403, '2023-10-14 02:17:40', 'C', 907);
                insert into store_order (id, created_at, payment_status, customer_id) values (404, '2023-10-14 23:36:11', 'C', 270);
                insert into store_order (id, created_at, payment_status, customer_id) values (405, '2024-05-07 18:32:56', 'F', 876);
                insert into store_order (id, created_at, payment_status, customer_id) values (406, '2023-09-09 12:32:08', 'P', 433);
                insert into store_order (id, created_at, payment_status, customer_id) values (407, '2024-01-30 17:48:11', 'C', 815);
                insert into store_order (id, created_at, payment_status, customer_id) values (408, '2022-12-30 07:26:00', 'P', 651);
                insert into store_order (id, created_at, payment_status, customer_id) values (409, '2023-08-17 07:01:27', 'P', 643);
                insert into store_order (id, created_at, payment_status, customer_id) values (410, '2024-03-27 23:46:45', 'C', 607);
                insert into store_order (id, created_at, payment_status, customer_id) values (411, '2024-04-16 13:53:05', 'C', 385);
                insert into store_order (id, created_at, payment_status, customer_id) values (412, '2023-11-25 16:59:06', 'C', 526);
                insert into store_order (id, created_at, payment_status, customer_id) values (413, '2022-11-15 06:32:31', 'C', 1000);
                insert into store_order (id, created_at, payment_status, customer_id) values (414, '2023-09-05 18:15:50', 'P', 274);
                insert into store_order (id, created_at, payment_status, customer_id) values (415, '2024-06-14 21:37:33', 'P', 440);
                insert into store_order (id, created_at, payment_status, customer_id) values (416, '2022-12-12 00:17:27', 'C', 433);
                insert into store_order (id, created_at, payment_status, customer_id) values (417, '2024-04-12 19:36:57', 'P', 634);
                insert into store_order (id, created_at, payment_status, customer_id) values (418, '2024-02-06 10:48:25', 'C', 345);
                insert into store_order (id, created_at, payment_status, customer_id) values (419, '2022-08-15 02:58:01', 'P', 294);
                insert into store_order (id, created_at, payment_status, customer_id) values (420, '2022-09-03 15:09:30', 'P', 947);
                insert into store_order (id, created_at, payment_status, customer_id) values (421, '2022-11-11 22:22:12', 'P', 740);
                insert into store_order (id, created_at, payment_status, customer_id) values (422, '2023-05-18 08:18:37', 'F', 903);
                insert into store_order (id, created_at, payment_status, customer_id) values (423, '2024-02-07 14:29:00', 'F', 479);
                insert into store_order (id, created_at, payment_status, customer_id) values (424, '2023-06-18 04:38:42', 'F', 756);
                insert into store_order (id, created_at, payment_status, customer_id) values (425, '2022-09-12 14:00:36', 'C', 617);
                insert into store_order (id, created_at, payment_status, customer_id) values (426, '2022-08-16 08:28:20', 'F', 443);
                insert into store_order (id, created_at, payment_status, customer_id) values (427, '2023-10-03 13:30:03', 'P', 900);
                insert into store_order (id, created_at, payment_status, customer_id) values (428, '2023-07-01 03:32:27', 'P', 601);
                insert into store_order (id, created_at, payment_status, customer_id) values (429, '2023-04-11 07:40:30', 'P', 714);
                insert into store_order (id, created_at, payment_status, customer_id) values (430, '2022-08-26 01:28:11', 'F', 290);
                insert into store_order (id, created_at, payment_status, customer_id) values (431, '2023-06-16 18:01:27', 'P', 864);
                insert into store_order (id, created_at, payment_status, customer_id) values (432, '2023-07-04 07:46:36', 'C', 487);
                insert into store_order (id, created_at, payment_status, customer_id) values (433, '2023-06-15 00:01:05', 'P', 637);
                insert into store_order (id, created_at, payment_status, customer_id) values (434, '2023-10-02 22:50:02', 'C', 663);
                insert into store_order (id, created_at, payment_status, customer_id) values (435, '2022-08-27 03:33:17', 'C', 770);
                insert into store_order (id, created_at, payment_status, customer_id) values (436, '2024-01-08 16:29:24', 'F', 573);
                insert into store_order (id, created_at, payment_status, customer_id) values (437, '2023-10-06 12:08:03', 'P', 372);
                insert into store_order (id, created_at, payment_status, customer_id) values (438, '2023-05-13 09:18:08', 'C', 713);
                insert into store_order (id, created_at, payment_status, customer_id) values (439, '2023-02-01 09:57:59', 'P', 232);
                insert into store_order (id, created_at, payment_status, customer_id) values (440, '2022-09-19 22:53:48', 'P', 28);
                insert into store_order (id, created_at, payment_status, customer_id) values (441, '2023-01-06 00:04:41', 'C', 420);
                insert into store_order (id, created_at, payment_status, customer_id) values (442, '2024-04-02 16:29:14', 'P', 390);
                insert into store_order (id, created_at, payment_status, customer_id) values (443, '2023-11-13 15:05:12', 'P', 61);
                insert into store_order (id, created_at, payment_status, customer_id) values (444, '2024-04-18 22:43:49', 'P', 4);
                insert into store_order (id, created_at, payment_status, customer_id) values (445, '2023-04-27 02:34:05', 'C', 471);
                insert into store_order (id, created_at, payment_status, customer_id) values (446, '2024-03-20 23:45:51', 'F', 475);
                insert into store_order (id, created_at, payment_status, customer_id) values (447, '2022-11-03 21:18:04', 'P', 961);
                insert into store_order (id, created_at, payment_status, customer_id) values (448, '2024-06-14 18:22:12', 'P', 357);
                insert into store_order (id, created_at, payment_status, customer_id) values (449, '2022-08-15 18:26:21', 'C', 86);
                insert into store_order (id, created_at, payment_status, customer_id) values (450, '2024-01-23 06:28:01', 'F', 794);
                insert into store_order (id, created_at, payment_status, customer_id) values (451, '2023-05-18 20:48:32', 'P', 644);
                insert into store_order (id, created_at, payment_status, customer_id) values (452, '2023-07-10 03:09:29', 'F', 577);
                insert into store_order (id, created_at, payment_status, customer_id) values (453, '2024-05-21 09:29:14', 'P', 708);
                insert into store_order (id, created_at, payment_status, customer_id) values (454, '2024-05-28 14:38:10', 'F', 856);
                insert into store_order (id, created_at, payment_status, customer_id) values (455, '2023-09-16 16:33:35', 'F', 910);
                insert into store_order (id, created_at, payment_status, customer_id) values (456, '2022-07-17 07:05:36', 'F', 209);
                insert into store_order (id, created_at, payment_status, customer_id) values (457, '2022-11-10 05:20:29', 'C', 15);
                insert into store_order (id, created_at, payment_status, customer_id) values (458, '2023-01-26 05:05:59', 'C', 683);
                insert into store_order (id, created_at, payment_status, customer_id) values (459, '2023-10-22 15:05:47', 'F', 468);
                insert into store_order (id, created_at, payment_status, customer_id) values (460, '2023-10-26 03:55:36', 'F', 495);
                insert into store_order (id, created_at, payment_status, customer_id) values (461, '2024-02-03 18:48:06', 'F', 616);
                insert into store_order (id, created_at, payment_status, customer_id) values (462, '2023-04-01 08:58:05', 'C', 381);
                insert into store_order (id, created_at, payment_status, customer_id) values (463, '2023-08-31 18:35:19', 'P', 128);
                insert into store_order (id, created_at, payment_status, customer_id) values (464, '2023-11-27 05:02:31', 'P', 179);
                insert into store_order (id, created_at, payment_status, customer_id) values (465, '2022-11-13 23:28:06', 'C', 684);
                insert into store_order (id, created_at, payment_status, customer_id) values (466, '2024-01-11 23:00:49', 'C', 670);
                insert into store_order (id, created_at, payment_status, customer_id) values (467, '2023-11-26 22:44:15', 'C', 510);
                insert into store_order (id, created_at, payment_status, customer_id) values (468, '2024-04-18 21:09:40', 'P', 134);
                insert into store_order (id, created_at, payment_status, customer_id) values (469, '2022-11-05 09:50:01', 'F', 749);
                insert into store_order (id, created_at, payment_status, customer_id) values (470, '2023-04-05 23:53:25', 'F', 214);
                insert into store_order (id, created_at, payment_status, customer_id) values (471, '2024-02-02 12:24:01', 'C', 976);
                insert into store_order (id, created_at, payment_status, customer_id) values (472, '2023-11-22 20:03:22', 'F', 898);
                insert into store_order (id, created_at, payment_status, customer_id) values (473, '2022-07-16 05:23:59', 'P', 842);
                insert into store_order (id, created_at, payment_status, customer_id) values (474, '2023-07-31 00:13:00', 'P', 502);
                insert into store_order (id, created_at, payment_status, customer_id) values (475, '2024-03-08 23:51:09', 'F', 566);
                insert into store_order (id, created_at, payment_status, customer_id) values (476, '2023-04-27 16:35:49', 'P', 181);
                insert into store_order (id, created_at, payment_status, customer_id) values (477, '2024-02-15 01:38:26', 'P', 434);
                insert into store_order (id, created_at, payment_status, customer_id) values (478, '2023-07-14 18:35:48', 'F', 323);
                insert into store_order (id, created_at, payment_status, customer_id) values (479, '2024-03-10 06:34:04', 'F', 822);
                insert into store_order (id, created_at, payment_status, customer_id) values (480, '2023-09-27 06:00:04', 'P', 932);
                insert into store_order (id, created_at, payment_status, customer_id) values (481, '2022-11-26 01:58:02', 'F', 865);
                insert into store_order (id, created_at, payment_status, customer_id) values (482, '2022-07-18 10:01:03', 'C', 629);
                insert into store_order (id, created_at, payment_status, customer_id) values (483, '2023-02-12 23:23:04', 'C', 966);
                insert into store_order (id, created_at, payment_status, customer_id) values (484, '2023-02-02 00:10:16', 'P', 249);
                insert into store_order (id, created_at, payment_status, customer_id) values (485, '2023-10-07 08:47:58', 'P', 562);
                insert into store_order (id, created_at, payment_status, customer_id) values (486, '2023-11-11 00:54:51', 'P', 991);
                insert into store_order (id, created_at, payment_status, customer_id) values (487, '2024-04-01 12:17:22', 'C', 440);
                insert into store_order (id, created_at, payment_status, customer_id) values (488, '2023-05-20 21:29:54', 'F', 306);
                insert into store_order (id, created_at, payment_status, customer_id) values (489, '2023-08-29 17:29:50', 'C', 258);
                insert into store_order (id, created_at, payment_status, customer_id) values (490, '2023-09-02 04:32:49', 'C', 717);
                insert into store_order (id, created_at, payment_status, customer_id) values (491, '2024-06-18 22:51:47', 'P', 126);
                insert into store_order (id, created_at, payment_status, customer_id) values (492, '2023-05-02 09:45:35', 'C', 586);
                insert into store_order (id, created_at, payment_status, customer_id) values (493, '2024-04-21 07:45:47', 'C', 468);
                insert into store_order (id, created_at, payment_status, customer_id) values (494, '2023-06-18 20:12:38', 'F', 736);
                insert into store_order (id, created_at, payment_status, customer_id) values (495, '2023-05-25 23:51:02', 'C', 329);
                insert into store_order (id, created_at, payment_status, customer_id) values (496, '2024-06-04 13:34:09', 'F', 483);
                insert into store_order (id, created_at, payment_status, customer_id) values (497, '2023-05-10 10:01:04', 'C', 768);
                insert into store_order (id, created_at, payment_status, customer_id) values (498, '2022-07-18 03:43:34', 'P', 913);
                insert into store_order (id, created_at, payment_status, customer_id) values (499, '2024-01-05 04:28:42', 'P', 20);
                insert into store_order (id, created_at, payment_status, customer_id) values (500, '2022-10-14 09:48:14', 'C', 573);
                insert into store_order (id, created_at, payment_status, customer_id) values (501, '2023-07-27 11:48:13', 'C', 214);
                insert into store_order (id, created_at, payment_status, customer_id) values (502, '2023-06-27 12:27:02', 'F', 412);
                insert into store_order (id, created_at, payment_status, customer_id) values (503, '2023-10-19 16:17:56', 'F', 736);
                insert into store_order (id, created_at, payment_status, customer_id) values (504, '2023-07-15 07:58:07', 'P', 413);
                insert into store_order (id, created_at, payment_status, customer_id) values (505, '2024-06-10 04:55:47', 'C', 639);
                insert into store_order (id, created_at, payment_status, customer_id) values (506, '2023-05-19 07:36:12', 'C', 488);
                insert into store_order (id, created_at, payment_status, customer_id) values (507, '2023-04-08 00:52:49', 'P', 319);
                insert into store_order (id, created_at, payment_status, customer_id) values (508, '2023-08-01 11:44:58', 'P', 503);
                insert into store_order (id, created_at, payment_status, customer_id) values (509, '2023-05-15 18:35:46', 'F', 864);
                insert into store_order (id, created_at, payment_status, customer_id) values (510, '2023-11-03 03:30:23', 'P', 930);
                insert into store_order (id, created_at, payment_status, customer_id) values (511, '2023-08-08 02:39:40', 'P', 510);
                insert into store_order (id, created_at, payment_status, customer_id) values (512, '2022-08-05 18:50:05', 'P', 915);
                insert into store_order (id, created_at, payment_status, customer_id) values (513, '2024-04-19 10:55:22', 'F', 813);
                insert into store_order (id, created_at, payment_status, customer_id) values (514, '2023-02-18 10:41:46', 'P', 242);
                insert into store_order (id, created_at, payment_status, customer_id) values (515, '2022-07-24 12:17:55', 'C', 397);
                insert into store_order (id, created_at, payment_status, customer_id) values (516, '2022-10-08 02:39:08', 'C', 904);
                insert into store_order (id, created_at, payment_status, customer_id) values (517, '2023-06-28 09:02:28', 'C', 124);
                insert into store_order (id, created_at, payment_status, customer_id) values (518, '2022-09-02 08:45:06', 'P', 494);
                insert into store_order (id, created_at, payment_status, customer_id) values (519, '2022-12-02 07:28:13', 'F', 465);
                insert into store_order (id, created_at, payment_status, customer_id) values (520, '2023-09-26 15:09:06', 'C', 101);
                insert into store_order (id, created_at, payment_status, customer_id) values (521, '2022-08-14 03:24:11', 'P', 765);
                insert into store_order (id, created_at, payment_status, customer_id) values (522, '2024-01-30 23:53:37', 'C', 57);
                insert into store_order (id, created_at, payment_status, customer_id) values (523, '2024-01-11 08:33:10', 'F', 564);
                insert into store_order (id, created_at, payment_status, customer_id) values (524, '2022-10-10 00:09:55', 'F', 400);
                insert into store_order (id, created_at, payment_status, customer_id) values (525, '2022-10-10 11:52:54', 'F', 2);
                insert into store_order (id, created_at, payment_status, customer_id) values (526, '2024-04-06 11:15:00', 'C', 381);
                insert into store_order (id, created_at, payment_status, customer_id) values (527, '2023-04-14 00:22:27', 'P', 804);
                insert into store_order (id, created_at, payment_status, customer_id) values (528, '2023-04-05 05:01:30', 'F', 141);
                insert into store_order (id, created_at, payment_status, customer_id) values (529, '2024-03-30 00:39:31', 'F', 35);
                insert into store_order (id, created_at, payment_status, customer_id) values (530, '2022-10-14 16:22:28', 'C', 239);
                insert into store_order (id, created_at, payment_status, customer_id) values (531, '2022-08-17 13:49:23', 'P', 210);
                insert into store_order (id, created_at, payment_status, customer_id) values (532, '2023-04-04 01:57:44', 'P', 49);
                insert into store_order (id, created_at, payment_status, customer_id) values (533, '2023-04-05 04:02:39', 'F', 832);
                insert into store_order (id, created_at, payment_status, customer_id) values (534, '2023-12-11 07:33:46', 'P', 407);
                insert into store_order (id, created_at, payment_status, customer_id) values (535, '2023-03-21 02:48:51', 'C', 92);
                insert into store_order (id, created_at, payment_status, customer_id) values (536, '2024-06-07 05:37:25', 'C', 302);
                insert into store_order (id, created_at, payment_status, customer_id) values (537, '2023-07-02 08:54:00', 'P', 641);
                insert into store_order (id, created_at, payment_status, customer_id) values (538, '2023-03-21 23:04:28', 'F', 940);
                insert into store_order (id, created_at, payment_status, customer_id) values (539, '2023-04-23 14:48:04', 'P', 567);
                insert into store_order (id, created_at, payment_status, customer_id) values (540, '2023-07-25 05:29:42', 'C', 980);
                insert into store_order (id, created_at, payment_status, customer_id) values (541, '2022-12-30 02:50:08', 'F', 501);
                insert into store_order (id, created_at, payment_status, customer_id) values (542, '2024-06-21 02:53:22', 'C', 322);
                insert into store_order (id, created_at, payment_status, customer_id) values (543, '2024-02-12 01:59:22', 'C', 287);
                insert into store_order (id, created_at, payment_status, customer_id) values (544, '2024-05-19 22:19:03', 'C', 578);
                insert into store_order (id, created_at, payment_status, customer_id) values (545, '2023-08-13 12:30:17', 'C', 986);
                insert into store_order (id, created_at, payment_status, customer_id) values (546, '2024-02-21 17:19:18', 'F', 603);
                insert into store_order (id, created_at, payment_status, customer_id) values (547, '2022-09-04 04:05:38', 'C', 853);
                insert into store_order (id, created_at, payment_status, customer_id) values (548, '2024-01-27 14:42:37', 'C', 745);
                insert into store_order (id, created_at, payment_status, customer_id) values (549, '2024-03-29 17:57:38', 'F', 503);
                insert into store_order (id, created_at, payment_status, customer_id) values (550, '2024-01-12 22:45:08', 'F', 266);
                insert into store_order (id, created_at, payment_status, customer_id) values (551, '2023-01-10 03:29:51', 'C', 134);
                insert into store_order (id, created_at, payment_status, customer_id) values (552, '2024-01-01 10:39:31', 'F', 567);
                insert into store_order (id, created_at, payment_status, customer_id) values (553, '2023-01-13 15:59:22', 'C', 818);
                insert into store_order (id, created_at, payment_status, customer_id) values (554, '2024-06-26 14:13:41', 'P', 301);
                insert into store_order (id, created_at, payment_status, customer_id) values (555, '2022-12-20 04:42:27', 'F', 689);
                insert into store_order (id, created_at, payment_status, customer_id) values (556, '2024-05-18 07:43:33', 'F', 804);
                insert into store_order (id, created_at, payment_status, customer_id) values (557, '2024-04-09 03:54:56', 'F', 428);
                insert into store_order (id, created_at, payment_status, customer_id) values (558, '2024-03-11 15:34:13', 'P', 423);
                insert into store_order (id, created_at, payment_status, customer_id) values (559, '2024-06-27 00:42:51', 'C', 28);
                insert into store_order (id, created_at, payment_status, customer_id) values (560, '2022-10-05 06:54:26', 'P', 917);
                insert into store_order (id, created_at, payment_status, customer_id) values (561, '2023-12-09 00:48:14', 'C', 760);
                insert into store_order (id, created_at, payment_status, customer_id) values (562, '2024-01-24 06:53:07', 'P', 385);
                insert into store_order (id, created_at, payment_status, customer_id) values (563, '2023-10-20 02:47:26', 'P', 986);
                insert into store_order (id, created_at, payment_status, customer_id) values (564, '2023-08-05 10:58:21', 'C', 741);
                insert into store_order (id, created_at, payment_status, customer_id) values (565, '2022-08-13 12:49:38', 'C', 273);
                insert into store_order (id, created_at, payment_status, customer_id) values (566, '2023-11-07 22:38:38', 'P', 54);
                insert into store_order (id, created_at, payment_status, customer_id) values (567, '2023-09-18 02:47:12', 'F', 473);
                insert into store_order (id, created_at, payment_status, customer_id) values (568, '2023-05-10 18:03:22', 'P', 713);
                insert into store_order (id, created_at, payment_status, customer_id) values (569, '2024-05-22 02:50:12', 'C', 939);
                insert into store_order (id, created_at, payment_status, customer_id) values (570, '2023-05-08 23:53:01', 'P', 800);
                insert into store_order (id, created_at, payment_status, customer_id) values (571, '2022-08-13 06:14:20', 'F', 418);
                insert into store_order (id, created_at, payment_status, customer_id) values (572, '2023-03-31 23:19:50', 'C', 196);
                insert into store_order (id, created_at, payment_status, customer_id) values (573, '2024-03-24 03:41:07', 'C', 211);
                insert into store_order (id, created_at, payment_status, customer_id) values (574, '2022-08-08 19:58:51', 'F', 867);
                insert into store_order (id, created_at, payment_status, customer_id) values (575, '2022-09-15 08:36:15', 'F', 279);
                insert into store_order (id, created_at, payment_status, customer_id) values (576, '2022-11-19 23:25:36', 'C', 469);
                insert into store_order (id, created_at, payment_status, customer_id) values (577, '2022-11-25 06:11:43', 'C', 928);
                insert into store_order (id, created_at, payment_status, customer_id) values (578, '2024-05-28 08:20:20', 'F', 138);
                insert into store_order (id, created_at, payment_status, customer_id) values (579, '2024-06-08 10:50:14', 'F', 715);
                insert into store_order (id, created_at, payment_status, customer_id) values (580, '2023-09-09 01:56:06', 'P', 848);
                insert into store_order (id, created_at, payment_status, customer_id) values (581, '2023-09-07 23:20:35', 'P', 361);
                insert into store_order (id, created_at, payment_status, customer_id) values (582, '2024-02-18 15:29:33', 'P', 812);
                insert into store_order (id, created_at, payment_status, customer_id) values (583, '2024-04-10 08:36:58', 'C', 686);
                insert into store_order (id, created_at, payment_status, customer_id) values (584, '2024-02-02 15:09:36', 'F', 621);
                insert into store_order (id, created_at, payment_status, customer_id) values (585, '2023-12-04 15:55:37', 'F', 740);
                insert into store_order (id, created_at, payment_status, customer_id) values (586, '2023-07-08 02:45:05', 'P', 167);
                insert into store_order (id, created_at, payment_status, customer_id) values (587, '2023-06-07 18:34:48', 'C', 4);
                insert into store_order (id, created_at, payment_status, customer_id) values (588, '2023-02-15 21:36:14', 'F', 325);
                insert into store_order (id, created_at, payment_status, customer_id) values (589, '2023-09-27 03:38:15', 'F', 560);
                insert into store_order (id, created_at, payment_status, customer_id) values (590, '2024-03-24 16:14:31', 'C', 336);
                insert into store_order (id, created_at, payment_status, customer_id) values (591, '2024-03-27 21:03:21', 'P', 94);
                insert into store_order (id, created_at, payment_status, customer_id) values (592, '2023-08-21 20:10:03', 'P', 590);
                insert into store_order (id, created_at, payment_status, customer_id) values (593, '2022-09-15 20:03:47', 'C', 263);
                insert into store_order (id, created_at, payment_status, customer_id) values (594, '2023-10-29 05:49:32', 'P', 932);
                insert into store_order (id, created_at, payment_status, customer_id) values (595, '2023-12-23 18:43:42', 'P', 861);
                insert into store_order (id, created_at, payment_status, customer_id) values (596, '2024-01-28 15:32:19', 'P', 529);
                insert into store_order (id, created_at, payment_status, customer_id) values (597, '2024-04-19 20:07:32', 'F', 11);
                insert into store_order (id, created_at, payment_status, customer_id) values (598, '2023-06-27 03:56:01', 'C', 631);
                insert into store_order (id, created_at, payment_status, customer_id) values (599, '2022-10-29 06:08:12', 'C', 768);
                insert into store_order (id, created_at, payment_status, customer_id) values (600, '2024-05-12 06:58:05', 'P', 196);
                insert into store_order (id, created_at, payment_status, customer_id) values (601, '2023-08-21 07:06:02', 'C', 785);
                insert into store_order (id, created_at, payment_status, customer_id) values (602, '2022-07-08 15:49:20', 'F', 860);
                insert into store_order (id, created_at, payment_status, customer_id) values (603, '2022-11-16 04:56:01', 'C', 855);
                insert into store_order (id, created_at, payment_status, customer_id) values (604, '2023-11-14 12:36:20', 'C', 32);
                insert into store_order (id, created_at, payment_status, customer_id) values (605, '2022-11-27 15:09:14', 'P', 748);
                insert into store_order (id, created_at, payment_status, customer_id) values (606, '2023-03-29 20:02:59', 'C', 536);
                insert into store_order (id, created_at, payment_status, customer_id) values (607, '2022-12-30 11:22:32', 'F', 934);
                insert into store_order (id, created_at, payment_status, customer_id) values (608, '2024-04-26 19:38:02', 'P', 552);
                insert into store_order (id, created_at, payment_status, customer_id) values (609, '2024-05-01 09:21:14', 'P', 360);
                insert into store_order (id, created_at, payment_status, customer_id) values (610, '2023-11-16 10:49:34', 'P', 187);
                insert into store_order (id, created_at, payment_status, customer_id) values (611, '2023-01-05 18:12:55', 'P', 681);
                insert into store_order (id, created_at, payment_status, customer_id) values (612, '2024-07-02 11:31:48', 'C', 872);
                insert into store_order (id, created_at, payment_status, customer_id) values (613, '2023-10-05 21:38:29', 'F', 709);
                insert into store_order (id, created_at, payment_status, customer_id) values (614, '2024-05-12 11:13:16', 'P', 50);
                insert into store_order (id, created_at, payment_status, customer_id) values (615, '2022-10-10 15:23:01', 'P', 227);
                insert into store_order (id, created_at, payment_status, customer_id) values (616, '2024-04-08 08:44:00', 'P', 563);
                insert into store_order (id, created_at, payment_status, customer_id) values (617, '2022-12-20 14:12:16', 'C', 866);
                insert into store_order (id, created_at, payment_status, customer_id) values (618, '2023-01-02 11:31:40', 'P', 283);
                insert into store_order (id, created_at, payment_status, customer_id) values (619, '2022-11-27 14:23:34', 'P', 377);
                insert into store_order (id, created_at, payment_status, customer_id) values (620, '2022-09-05 04:26:06', 'C', 914);
                insert into store_order (id, created_at, payment_status, customer_id) values (621, '2024-01-30 08:41:56', 'F', 13);
                insert into store_order (id, created_at, payment_status, customer_id) values (622, '2024-01-30 00:45:27', 'F', 162);
                insert into store_order (id, created_at, payment_status, customer_id) values (623, '2023-05-27 03:36:28', 'P', 678);
                insert into store_order (id, created_at, payment_status, customer_id) values (624, '2023-05-05 09:35:50', 'P', 790);
                insert into store_order (id, created_at, payment_status, customer_id) values (625, '2023-01-22 02:13:20', 'P', 400);
                insert into store_order (id, created_at, payment_status, customer_id) values (626, '2024-06-30 03:15:50', 'P', 217);
                insert into store_order (id, created_at, payment_status, customer_id) values (627, '2024-01-30 17:19:36', 'P', 161);
                insert into store_order (id, created_at, payment_status, customer_id) values (628, '2024-03-25 00:51:39', 'P', 862);
                insert into store_order (id, created_at, payment_status, customer_id) values (629, '2023-10-04 13:01:23', 'F', 863);
                insert into store_order (id, created_at, payment_status, customer_id) values (630, '2023-06-30 03:00:57', 'F', 71);
                insert into store_order (id, created_at, payment_status, customer_id) values (631, '2023-12-30 00:52:00', 'F', 500);
                insert into store_order (id, created_at, payment_status, customer_id) values (632, '2024-01-13 16:12:55', 'F', 92);
                insert into store_order (id, created_at, payment_status, customer_id) values (633, '2024-01-09 17:36:15', 'P', 781);
                insert into store_order (id, created_at, payment_status, customer_id) values (634, '2023-03-21 00:35:41', 'C', 985);
                insert into store_order (id, created_at, payment_status, customer_id) values (635, '2024-04-16 15:48:08', 'C', 196);
                insert into store_order (id, created_at, payment_status, customer_id) values (636, '2023-04-08 19:26:01', 'C', 168);
                insert into store_order (id, created_at, payment_status, customer_id) values (637, '2024-03-19 13:50:03', 'P', 286);
                insert into store_order (id, created_at, payment_status, customer_id) values (638, '2023-05-09 05:29:59', 'P', 622);
                insert into store_order (id, created_at, payment_status, customer_id) values (639, '2022-08-18 13:27:44', 'C', 765);
                insert into store_order (id, created_at, payment_status, customer_id) values (640, '2022-12-15 07:02:07', 'F', 770);
                insert into store_order (id, created_at, payment_status, customer_id) values (641, '2022-11-21 23:54:34', 'F', 337);
                insert into store_order (id, created_at, payment_status, customer_id) values (642, '2023-04-01 13:23:24', 'P', 555);
                insert into store_order (id, created_at, payment_status, customer_id) values (643, '2023-07-24 22:45:26', 'P', 784);
                insert into store_order (id, created_at, payment_status, customer_id) values (644, '2022-07-28 09:39:53', 'P', 680);
                insert into store_order (id, created_at, payment_status, customer_id) values (645, '2023-11-16 12:42:06', 'C', 39);
                insert into store_order (id, created_at, payment_status, customer_id) values (646, '2022-11-06 15:13:21', 'C', 458);
                insert into store_order (id, created_at, payment_status, customer_id) values (647, '2023-04-18 21:18:55', 'F', 89);
                insert into store_order (id, created_at, payment_status, customer_id) values (648, '2023-05-17 00:16:29', 'P', 278);
                insert into store_order (id, created_at, payment_status, customer_id) values (649, '2023-03-15 14:50:22', 'P', 598);
                insert into store_order (id, created_at, payment_status, customer_id) values (650, '2024-04-28 12:07:05', 'P', 627);
                insert into store_order (id, created_at, payment_status, customer_id) values (651, '2023-11-11 08:37:36', 'C', 645);
                insert into store_order (id, created_at, payment_status, customer_id) values (652, '2022-09-14 07:30:11', 'C', 197);
                insert into store_order (id, created_at, payment_status, customer_id) values (653, '2023-03-10 16:19:00', 'C', 672);
                insert into store_order (id, created_at, payment_status, customer_id) values (654, '2023-08-29 13:05:49', 'P', 330);
                insert into store_order (id, created_at, payment_status, customer_id) values (655, '2023-09-19 05:41:26', 'P', 413);
                insert into store_order (id, created_at, payment_status, customer_id) values (656, '2023-11-08 15:11:37', 'P', 412);
                insert into store_order (id, created_at, payment_status, customer_id) values (657, '2023-09-19 10:57:42', 'P', 920);
                insert into store_order (id, created_at, payment_status, customer_id) values (658, '2023-02-22 18:31:57', 'F', 406);
                insert into store_order (id, created_at, payment_status, customer_id) values (659, '2023-02-26 05:57:27', 'C', 600);
                insert into store_order (id, created_at, payment_status, customer_id) values (660, '2023-01-23 12:29:21', 'P', 253);
                insert into store_order (id, created_at, payment_status, customer_id) values (661, '2023-12-29 12:05:58', 'P', 626);
                insert into store_order (id, created_at, payment_status, customer_id) values (662, '2022-08-02 12:20:25', 'P', 735);
                insert into store_order (id, created_at, payment_status, customer_id) values (663, '2023-06-23 11:27:46', 'F', 179);
                insert into store_order (id, created_at, payment_status, customer_id) values (664, '2022-10-01 05:03:54', 'C', 187);
                insert into store_order (id, created_at, payment_status, customer_id) values (665, '2023-02-11 06:35:22', 'P', 333);
                insert into store_order (id, created_at, payment_status, customer_id) values (666, '2024-06-08 13:54:52', 'F', 588);
                insert into store_order (id, created_at, payment_status, customer_id) values (667, '2023-06-13 18:01:36', 'C', 903);
                insert into store_order (id, created_at, payment_status, customer_id) values (668, '2023-06-23 20:13:27', 'C', 250);
                insert into store_order (id, created_at, payment_status, customer_id) values (669, '2024-05-14 21:02:42', 'F', 863);
                insert into store_order (id, created_at, payment_status, customer_id) values (670, '2024-03-01 02:27:32', 'P', 515);
                insert into store_order (id, created_at, payment_status, customer_id) values (671, '2023-05-10 23:24:19', 'P', 49);
                insert into store_order (id, created_at, payment_status, customer_id) values (672, '2022-11-25 10:16:11', 'C', 981);
                insert into store_order (id, created_at, payment_status, customer_id) values (673, '2023-11-16 10:57:34', 'P', 721);
                insert into store_order (id, created_at, payment_status, customer_id) values (674, '2024-04-16 15:11:16', 'C', 463);
                insert into store_order (id, created_at, payment_status, customer_id) values (675, '2023-02-05 03:03:24', 'C', 680);
                insert into store_order (id, created_at, payment_status, customer_id) values (676, '2024-04-30 05:06:13', 'P', 110);
                insert into store_order (id, created_at, payment_status, customer_id) values (677, '2022-10-11 02:48:51', 'F', 45);
                insert into store_order (id, created_at, payment_status, customer_id) values (678, '2024-04-16 17:12:50', 'C', 639);
                insert into store_order (id, created_at, payment_status, customer_id) values (679, '2024-02-09 19:07:13', 'P', 577);
                insert into store_order (id, created_at, payment_status, customer_id) values (680, '2022-12-13 18:21:34', 'C', 414);
                insert into store_order (id, created_at, payment_status, customer_id) values (681, '2023-07-20 15:30:34', 'P', 461);
                insert into store_order (id, created_at, payment_status, customer_id) values (682, '2024-05-11 16:29:33', 'F', 364);
                insert into store_order (id, created_at, payment_status, customer_id) values (683, '2023-04-19 00:50:49', 'C', 25);
                insert into store_order (id, created_at, payment_status, customer_id) values (684, '2024-06-07 11:34:23', 'P', 762);
                insert into store_order (id, created_at, payment_status, customer_id) values (685, '2023-09-17 17:08:30', 'C', 892);
                insert into store_order (id, created_at, payment_status, customer_id) values (686, '2022-07-11 17:55:04', 'P', 580);
                insert into store_order (id, created_at, payment_status, customer_id) values (687, '2022-08-26 17:43:44', 'C', 577);
                insert into store_order (id, created_at, payment_status, customer_id) values (688, '2024-02-19 13:42:22', 'P', 37);
                insert into store_order (id, created_at, payment_status, customer_id) values (689, '2022-08-18 03:08:54', 'C', 719);
                insert into store_order (id, created_at, payment_status, customer_id) values (690, '2024-03-11 05:26:49', 'P', 14);
                insert into store_order (id, created_at, payment_status, customer_id) values (691, '2023-01-23 20:22:11', 'C', 283);
                insert into store_order (id, created_at, payment_status, customer_id) values (692, '2023-01-07 16:43:21', 'C', 190);
                insert into store_order (id, created_at, payment_status, customer_id) values (693, '2024-01-05 12:31:34', 'F', 27);
                insert into store_order (id, created_at, payment_status, customer_id) values (694, '2022-07-15 05:03:10', 'F', 156);
                insert into store_order (id, created_at, payment_status, customer_id) values (695, '2022-11-03 01:45:10', 'C', 253);
                insert into store_order (id, created_at, payment_status, customer_id) values (696, '2024-05-05 23:41:39', 'C', 549);
                insert into store_order (id, created_at, payment_status, customer_id) values (697, '2023-02-04 05:50:52', 'F', 78);
                insert into store_order (id, created_at, payment_status, customer_id) values (698, '2023-12-12 11:30:22', 'F', 712);
                insert into store_order (id, created_at, payment_status, customer_id) values (699, '2022-10-14 15:01:00', 'F', 656);
                insert into store_order (id, created_at, payment_status, customer_id) values (700, '2024-03-30 10:42:17', 'P', 700);
                insert into store_order (id, created_at, payment_status, customer_id) values (701, '2023-07-01 04:50:05', 'C', 738);
                insert into store_order (id, created_at, payment_status, customer_id) values (702, '2024-01-06 01:42:08', 'C', 266);
                insert into store_order (id, created_at, payment_status, customer_id) values (703, '2023-12-19 00:31:40', 'F', 593);
                insert into store_order (id, created_at, payment_status, customer_id) values (704, '2023-08-11 19:03:19', 'C', 431);
                insert into store_order (id, created_at, payment_status, customer_id) values (705, '2022-08-19 19:11:21', 'F', 613);
                insert into store_order (id, created_at, payment_status, customer_id) values (706, '2022-08-19 11:14:26', 'P', 353);
                insert into store_order (id, created_at, payment_status, customer_id) values (707, '2023-05-11 06:53:26', 'F', 154);
                insert into store_order (id, created_at, payment_status, customer_id) values (708, '2022-11-08 15:11:32', 'F', 801);
                insert into store_order (id, created_at, payment_status, customer_id) values (709, '2024-06-22 16:17:51', 'C', 958);
                insert into store_order (id, created_at, payment_status, customer_id) values (710, '2024-03-23 23:02:03', 'F', 877);
                insert into store_order (id, created_at, payment_status, customer_id) values (711, '2023-08-15 01:38:16', 'F', 113);
                insert into store_order (id, created_at, payment_status, customer_id) values (712, '2022-10-06 19:31:50', 'C', 284);
                insert into store_order (id, created_at, payment_status, customer_id) values (713, '2023-08-31 11:04:41', 'F', 767);
                insert into store_order (id, created_at, payment_status, customer_id) values (714, '2024-04-10 21:40:32', 'P', 427);
                insert into store_order (id, created_at, payment_status, customer_id) values (715, '2023-11-21 01:23:05', 'C', 483);
                insert into store_order (id, created_at, payment_status, customer_id) values (716, '2023-08-23 19:23:30', 'C', 74);
                insert into store_order (id, created_at, payment_status, customer_id) values (717, '2024-05-06 08:40:22', 'C', 677);
                insert into store_order (id, created_at, payment_status, customer_id) values (718, '2023-03-23 05:07:18', 'C', 650);
                insert into store_order (id, created_at, payment_status, customer_id) values (719, '2022-08-11 22:41:41', 'P', 942);
                insert into store_order (id, created_at, payment_status, customer_id) values (720, '2023-07-12 13:39:55', 'F', 636);
                insert into store_order (id, created_at, payment_status, customer_id) values (721, '2023-06-29 18:19:26', 'F', 813);
                insert into store_order (id, created_at, payment_status, customer_id) values (722, '2024-06-10 09:13:41', 'F', 969);
                insert into store_order (id, created_at, payment_status, customer_id) values (723, '2023-11-08 18:23:12', 'F', 125);
                insert into store_order (id, created_at, payment_status, customer_id) values (724, '2023-10-29 23:55:45', 'P', 141);
                insert into store_order (id, created_at, payment_status, customer_id) values (725, '2023-04-11 03:05:09', 'F', 157);
                insert into store_order (id, created_at, payment_status, customer_id) values (726, '2022-09-05 22:38:51', 'F', 924);
                insert into store_order (id, created_at, payment_status, customer_id) values (727, '2023-08-04 00:44:24', 'F', 734);
                insert into store_order (id, created_at, payment_status, customer_id) values (728, '2024-02-24 21:44:38', 'F', 522);
                insert into store_order (id, created_at, payment_status, customer_id) values (729, '2024-04-20 17:58:46', 'P', 138);
                insert into store_order (id, created_at, payment_status, customer_id) values (730, '2023-05-18 09:00:54', 'C', 314);
                insert into store_order (id, created_at, payment_status, customer_id) values (731, '2023-12-27 18:46:49', 'P', 942);
                insert into store_order (id, created_at, payment_status, customer_id) values (732, '2022-11-06 00:24:34', 'F', 511);
                insert into store_order (id, created_at, payment_status, customer_id) values (733, '2024-03-20 23:06:55', 'C', 626);
                insert into store_order (id, created_at, payment_status, customer_id) values (734, '2024-06-18 22:54:10', 'C', 460);
                insert into store_order (id, created_at, payment_status, customer_id) values (735, '2024-01-04 20:32:19', 'F', 867);
                insert into store_order (id, created_at, payment_status, customer_id) values (736, '2022-12-07 15:15:52', 'C', 344);
                insert into store_order (id, created_at, payment_status, customer_id) values (737, '2024-03-10 05:16:09', 'P', 718);
                insert into store_order (id, created_at, payment_status, customer_id) values (738, '2023-11-10 22:35:41', 'C', 5);
                insert into store_order (id, created_at, payment_status, customer_id) values (739, '2023-08-07 17:07:22', 'P', 362);
                insert into store_order (id, created_at, payment_status, customer_id) values (740, '2022-07-09 15:57:40', 'P', 345);
                insert into store_order (id, created_at, payment_status, customer_id) values (741, '2024-01-02 00:35:54', 'C', 287);
                insert into store_order (id, created_at, payment_status, customer_id) values (742, '2023-02-25 06:43:10', 'F', 268);
                insert into store_order (id, created_at, payment_status, customer_id) values (743, '2022-09-26 02:59:10', 'C', 650);
                insert into store_order (id, created_at, payment_status, customer_id) values (744, '2023-11-11 11:58:18', 'P', 277);
                insert into store_order (id, created_at, payment_status, customer_id) values (745, '2024-06-19 13:56:21', 'P', 40);
                insert into store_order (id, created_at, payment_status, customer_id) values (746, '2024-02-16 18:06:29', 'P', 166);
                insert into store_order (id, created_at, payment_status, customer_id) values (747, '2023-01-17 06:50:10', 'F', 926);
                insert into store_order (id, created_at, payment_status, customer_id) values (748, '2022-08-29 09:35:13', 'C', 69);
                insert into store_order (id, created_at, payment_status, customer_id) values (749, '2023-02-26 22:36:30', 'P', 891);
                insert into store_order (id, created_at, payment_status, customer_id) values (750, '2022-12-12 19:25:25', 'C', 601);
                insert into store_order (id, created_at, payment_status, customer_id) values (751, '2023-08-08 15:41:46', 'F', 343);
                insert into store_order (id, created_at, payment_status, customer_id) values (752, '2023-09-22 07:20:13', 'F', 228);
                insert into store_order (id, created_at, payment_status, customer_id) values (753, '2023-01-15 10:19:38', 'F', 319);
                insert into store_order (id, created_at, payment_status, customer_id) values (754, '2023-07-02 04:00:38', 'C', 992);
                insert into store_order (id, created_at, payment_status, customer_id) values (755, '2024-05-17 23:22:18', 'C', 177);
                insert into store_order (id, created_at, payment_status, customer_id) values (756, '2023-06-30 17:06:14', 'P', 48);
                insert into store_order (id, created_at, payment_status, customer_id) values (757, '2022-10-22 07:45:30', 'C', 156);
                insert into store_order (id, created_at, payment_status, customer_id) values (758, '2023-01-28 15:07:41', 'F', 70);
                insert into store_order (id, created_at, payment_status, customer_id) values (759, '2022-07-11 10:57:33', 'F', 93);
                insert into store_order (id, created_at, payment_status, customer_id) values (760, '2023-09-13 13:49:59', 'F', 733);
                insert into store_order (id, created_at, payment_status, customer_id) values (761, '2023-04-27 02:17:42', 'C', 711);
                insert into store_order (id, created_at, payment_status, customer_id) values (762, '2024-07-02 02:02:08', 'C', 69);
                insert into store_order (id, created_at, payment_status, customer_id) values (763, '2024-05-13 04:36:11', 'F', 284);
                insert into store_order (id, created_at, payment_status, customer_id) values (764, '2023-08-28 07:11:05', 'C', 844);
                insert into store_order (id, created_at, payment_status, customer_id) values (765, '2024-05-11 16:16:07', 'F', 729);
                insert into store_order (id, created_at, payment_status, customer_id) values (766, '2022-11-02 15:50:38', 'C', 359);
                insert into store_order (id, created_at, payment_status, customer_id) values (767, '2023-02-15 12:07:12', 'F', 105);
                insert into store_order (id, created_at, payment_status, customer_id) values (768, '2022-10-26 10:23:45', 'P', 139);
                insert into store_order (id, created_at, payment_status, customer_id) values (769, '2022-09-05 20:01:14', 'C', 217);
                insert into store_order (id, created_at, payment_status, customer_id) values (770, '2023-02-25 03:37:28', 'C', 424);
                insert into store_order (id, created_at, payment_status, customer_id) values (771, '2024-05-23 12:21:51', 'P', 499);
                insert into store_order (id, created_at, payment_status, customer_id) values (772, '2023-08-08 08:27:38', 'P', 227);
                insert into store_order (id, created_at, payment_status, customer_id) values (773, '2022-12-30 02:01:15', 'P', 665);
                insert into store_order (id, created_at, payment_status, customer_id) values (774, '2023-12-26 01:02:06', 'F', 579);
                insert into store_order (id, created_at, payment_status, customer_id) values (775, '2023-12-17 16:14:26', 'F', 212);
                insert into store_order (id, created_at, payment_status, customer_id) values (776, '2022-08-09 23:02:31', 'C', 308);
                insert into store_order (id, created_at, payment_status, customer_id) values (777, '2023-05-02 01:28:44', 'C', 644);
                insert into store_order (id, created_at, payment_status, customer_id) values (778, '2024-03-25 17:34:07', 'F', 552);
                insert into store_order (id, created_at, payment_status, customer_id) values (779, '2023-06-23 13:36:57', 'P', 118);
                insert into store_order (id, created_at, payment_status, customer_id) values (780, '2023-08-15 12:54:03', 'P', 81);
                insert into store_order (id, created_at, payment_status, customer_id) values (781, '2023-07-12 10:21:56', 'P', 886);
                insert into store_order (id, created_at, payment_status, customer_id) values (782, '2024-02-10 00:20:52', 'P', 948);
                insert into store_order (id, created_at, payment_status, customer_id) values (783, '2023-08-16 21:31:43', 'F', 374);
                insert into store_order (id, created_at, payment_status, customer_id) values (784, '2023-09-03 11:39:16', 'C', 288);
                insert into store_order (id, created_at, payment_status, customer_id) values (785, '2023-01-06 01:01:38', 'C', 626);
                insert into store_order (id, created_at, payment_status, customer_id) values (786, '2023-07-18 00:52:27', 'F', 850);
                insert into store_order (id, created_at, payment_status, customer_id) values (787, '2023-06-03 18:22:32', 'C', 629);
                insert into store_order (id, created_at, payment_status, customer_id) values (788, '2023-08-19 16:12:28', 'C', 553);
                insert into store_order (id, created_at, payment_status, customer_id) values (789, '2022-12-15 11:31:20', 'F', 986);
                insert into store_order (id, created_at, payment_status, customer_id) values (790, '2022-08-05 05:50:31', 'C', 304);
                insert into store_order (id, created_at, payment_status, customer_id) values (791, '2022-07-13 22:43:57', 'C', 113);
                insert into store_order (id, created_at, payment_status, customer_id) values (792, '2024-03-02 21:42:52', 'P', 140);
                insert into store_order (id, created_at, payment_status, customer_id) values (793, '2023-05-26 04:33:11', 'P', 373);
                insert into store_order (id, created_at, payment_status, customer_id) values (794, '2024-06-15 04:49:10', 'F', 618);
                insert into store_order (id, created_at, payment_status, customer_id) values (795, '2024-02-15 04:01:34', 'C', 200);
                insert into store_order (id, created_at, payment_status, customer_id) values (796, '2023-11-18 14:17:06', 'P', 840);
                insert into store_order (id, created_at, payment_status, customer_id) values (797, '2023-11-16 05:30:17', 'C', 786);
                insert into store_order (id, created_at, payment_status, customer_id) values (798, '2022-11-24 08:34:11', 'F', 645);
                insert into store_order (id, created_at, payment_status, customer_id) values (799, '2024-03-10 12:34:40', 'P', 256);
                insert into store_order (id, created_at, payment_status, customer_id) values (800, '2024-05-26 04:22:54', 'C', 488);
                insert into store_order (id, created_at, payment_status, customer_id) values (801, '2023-11-12 15:55:45', 'P', 58);
                insert into store_order (id, created_at, payment_status, customer_id) values (802, '2023-03-30 18:14:50', 'F', 724);
                insert into store_order (id, created_at, payment_status, customer_id) values (803, '2023-05-01 10:23:10', 'F', 144);
                insert into store_order (id, created_at, payment_status, customer_id) values (804, '2022-09-15 23:36:55', 'C', 582);
                insert into store_order (id, created_at, payment_status, customer_id) values (805, '2024-05-13 05:33:25', 'C', 254);
                insert into store_order (id, created_at, payment_status, customer_id) values (806, '2023-10-22 16:49:33', 'C', 505);
                insert into store_order (id, created_at, payment_status, customer_id) values (807, '2024-07-06 18:56:29', 'F', 816);
                insert into store_order (id, created_at, payment_status, customer_id) values (808, '2023-11-09 04:07:15', 'F', 455);
                insert into store_order (id, created_at, payment_status, customer_id) values (809, '2024-04-02 16:21:38', 'C', 736);
                insert into store_order (id, created_at, payment_status, customer_id) values (810, '2022-12-12 14:08:34', 'P', 921);
                insert into store_order (id, created_at, payment_status, customer_id) values (811, '2022-08-06 08:32:34', 'C', 650);
                insert into store_order (id, created_at, payment_status, customer_id) values (812, '2024-06-11 07:13:47', 'F', 311);
                insert into store_order (id, created_at, payment_status, customer_id) values (813, '2022-10-29 02:41:02', 'P', 895);
                insert into store_order (id, created_at, payment_status, customer_id) values (814, '2023-02-25 18:05:19', 'C', 495);
                insert into store_order (id, created_at, payment_status, customer_id) values (815, '2023-10-06 06:54:40', 'P', 550);
                insert into store_order (id, created_at, payment_status, customer_id) values (816, '2023-09-26 15:18:32', 'P', 399);
                insert into store_order (id, created_at, payment_status, customer_id) values (817, '2023-12-24 07:20:56', 'P', 519);
                insert into store_order (id, created_at, payment_status, customer_id) values (818, '2023-06-20 17:28:56', 'F', 108);
                insert into store_order (id, created_at, payment_status, customer_id) values (819, '2023-08-26 02:42:49', 'P', 684);
                insert into store_order (id, created_at, payment_status, customer_id) values (820, '2024-05-10 15:46:10', 'C', 513);
                insert into store_order (id, created_at, payment_status, customer_id) values (821, '2024-01-27 03:48:07', 'F', 403);
                insert into store_order (id, created_at, payment_status, customer_id) values (822, '2022-11-16 03:58:45', 'P', 589);
                insert into store_order (id, created_at, payment_status, customer_id) values (823, '2022-12-07 05:49:14', 'C', 690);
                insert into store_order (id, created_at, payment_status, customer_id) values (824, '2024-04-19 03:02:02', 'P', 651);
                insert into store_order (id, created_at, payment_status, customer_id) values (825, '2023-07-17 22:06:57', 'F', 333);
                insert into store_order (id, created_at, payment_status, customer_id) values (826, '2023-03-01 22:24:58', 'F', 645);
                insert into store_order (id, created_at, payment_status, customer_id) values (827, '2022-12-09 20:40:06', 'F', 651);
                insert into store_order (id, created_at, payment_status, customer_id) values (828, '2022-12-24 13:55:29', 'F', 135);
                insert into store_order (id, created_at, payment_status, customer_id) values (829, '2024-03-29 15:04:56', 'P', 330);
                insert into store_order (id, created_at, payment_status, customer_id) values (830, '2022-12-30 02:14:43', 'P', 491);
                insert into store_order (id, created_at, payment_status, customer_id) values (831, '2022-10-18 08:46:00', 'P', 376);
                insert into store_order (id, created_at, payment_status, customer_id) values (832, '2022-10-18 16:04:22', 'F', 293);
                insert into store_order (id, created_at, payment_status, customer_id) values (833, '2022-10-13 10:18:03', 'P', 227);
                insert into store_order (id, created_at, payment_status, customer_id) values (834, '2023-03-01 14:21:53', 'P', 168);
                insert into store_order (id, created_at, payment_status, customer_id) values (835, '2023-07-19 18:38:45', 'C', 41);
                insert into store_order (id, created_at, payment_status, customer_id) values (836, '2023-11-05 16:45:22', 'P', 956);
                insert into store_order (id, created_at, payment_status, customer_id) values (837, '2023-11-20 19:29:07', 'F', 775);
                insert into store_order (id, created_at, payment_status, customer_id) values (838, '2024-06-21 18:41:20', 'C', 243);
                insert into store_order (id, created_at, payment_status, customer_id) values (839, '2023-05-07 23:04:17', 'C', 719);
                insert into store_order (id, created_at, payment_status, customer_id) values (840, '2023-02-14 10:36:21', 'F', 548);
                insert into store_order (id, created_at, payment_status, customer_id) values (841, '2023-09-12 04:15:16', 'P', 81);
                insert into store_order (id, created_at, payment_status, customer_id) values (842, '2024-02-07 02:34:05', 'C', 891);
                insert into store_order (id, created_at, payment_status, customer_id) values (843, '2022-12-23 14:09:48', 'C', 963);
                insert into store_order (id, created_at, payment_status, customer_id) values (844, '2022-09-07 06:33:15', 'F', 723);
                insert into store_order (id, created_at, payment_status, customer_id) values (845, '2023-03-07 03:01:15', 'C', 545);
                insert into store_order (id, created_at, payment_status, customer_id) values (846, '2023-04-29 15:50:46', 'F', 88);
                insert into store_order (id, created_at, payment_status, customer_id) values (847, '2022-08-03 02:37:22', 'F', 523);
                insert into store_order (id, created_at, payment_status, customer_id) values (848, '2022-12-03 02:10:16', 'C', 578);
                insert into store_order (id, created_at, payment_status, customer_id) values (849, '2022-12-15 20:06:58', 'C', 713);
                insert into store_order (id, created_at, payment_status, customer_id) values (850, '2024-03-04 17:09:56', 'F', 477);
                insert into store_order (id, created_at, payment_status, customer_id) values (851, '2023-04-04 22:16:30', 'P', 134);
                insert into store_order (id, created_at, payment_status, customer_id) values (852, '2022-08-25 15:40:50', 'C', 212);
                insert into store_order (id, created_at, payment_status, customer_id) values (853, '2023-07-31 12:18:41', 'C', 858);
                insert into store_order (id, created_at, payment_status, customer_id) values (854, '2024-02-07 23:29:34', 'P', 802);
                insert into store_order (id, created_at, payment_status, customer_id) values (855, '2022-11-16 01:17:04', 'F', 715);
                insert into store_order (id, created_at, payment_status, customer_id) values (856, '2024-02-03 02:20:56', 'C', 747);
                insert into store_order (id, created_at, payment_status, customer_id) values (857, '2023-10-30 18:07:29', 'C', 9);
                insert into store_order (id, created_at, payment_status, customer_id) values (858, '2023-07-20 14:08:21', 'C', 29);
                insert into store_order (id, created_at, payment_status, customer_id) values (859, '2024-03-08 08:04:26', 'F', 788);
                insert into store_order (id, created_at, payment_status, customer_id) values (860, '2022-10-29 19:45:27', 'C', 234);
                insert into store_order (id, created_at, payment_status, customer_id) values (861, '2022-09-12 06:43:22', 'P', 877);
                insert into store_order (id, created_at, payment_status, customer_id) values (862, '2022-10-27 21:00:54', 'F', 657);
                insert into store_order (id, created_at, payment_status, customer_id) values (863, '2023-05-18 06:55:42', 'C', 226);
                insert into store_order (id, created_at, payment_status, customer_id) values (864, '2022-11-07 22:23:53', 'P', 452);
                insert into store_order (id, created_at, payment_status, customer_id) values (865, '2023-11-05 08:24:49', 'C', 851);
                insert into store_order (id, created_at, payment_status, customer_id) values (866, '2022-11-16 08:36:29', 'P', 73);
                insert into store_order (id, created_at, payment_status, customer_id) values (867, '2023-04-09 00:20:06', 'F', 750);
                insert into store_order (id, created_at, payment_status, customer_id) values (868, '2022-08-18 21:10:15', 'F', 53);
                insert into store_order (id, created_at, payment_status, customer_id) values (869, '2023-08-08 01:39:16', 'P', 760);
                insert into store_order (id, created_at, payment_status, customer_id) values (870, '2023-11-23 15:15:37', 'C', 909);
                insert into store_order (id, created_at, payment_status, customer_id) values (871, '2023-05-15 05:47:38', 'F', 123);
                insert into store_order (id, created_at, payment_status, customer_id) values (872, '2023-04-07 08:02:58', 'C', 521);
                insert into store_order (id, created_at, payment_status, customer_id) values (873, '2023-10-23 16:01:49', 'P', 87);
                insert into store_order (id, created_at, payment_status, customer_id) values (874, '2023-04-15 22:28:20', 'P', 556);
                insert into store_order (id, created_at, payment_status, customer_id) values (875, '2024-06-27 20:03:34', 'C', 70);
                insert into store_order (id, created_at, payment_status, customer_id) values (876, '2023-05-12 09:41:05', 'C', 447);
                insert into store_order (id, created_at, payment_status, customer_id) values (877, '2024-01-15 22:07:04', 'C', 897);
                insert into store_order (id, created_at, payment_status, customer_id) values (878, '2022-11-11 12:44:22', 'P', 703);
                insert into store_order (id, created_at, payment_status, customer_id) values (879, '2023-07-26 06:18:59', 'F', 193);
                insert into store_order (id, created_at, payment_status, customer_id) values (880, '2024-02-01 13:23:54', 'P', 423);
                insert into store_order (id, created_at, payment_status, customer_id) values (881, '2022-07-15 13:55:10', 'C', 925);
                insert into store_order (id, created_at, payment_status, customer_id) values (882, '2023-09-24 21:49:37', 'P', 41);
                insert into store_order (id, created_at, payment_status, customer_id) values (883, '2023-07-02 00:32:01', 'C', 45);
                insert into store_order (id, created_at, payment_status, customer_id) values (884, '2023-08-07 13:04:48', 'P', 360);
                insert into store_order (id, created_at, payment_status, customer_id) values (885, '2022-10-30 04:06:51', 'C', 904);
                insert into store_order (id, created_at, payment_status, customer_id) values (886, '2022-08-23 06:27:01', 'F', 687);
                insert into store_order (id, created_at, payment_status, customer_id) values (887, '2022-11-01 00:03:36', 'P', 546);
                insert into store_order (id, created_at, payment_status, customer_id) values (888, '2023-11-18 11:54:30', 'P', 429);
                insert into store_order (id, created_at, payment_status, customer_id) values (889, '2023-10-21 17:20:10', 'C', 352);
                insert into store_order (id, created_at, payment_status, customer_id) values (890, '2022-11-21 02:33:54', 'F', 480);
                insert into store_order (id, created_at, payment_status, customer_id) values (891, '2022-12-16 23:18:42', 'F', 878);
                insert into store_order (id, created_at, payment_status, customer_id) values (892, '2022-11-28 03:36:43', 'F', 627);
                insert into store_order (id, created_at, payment_status, customer_id) values (893, '2024-02-27 09:51:00', 'F', 812);
                insert into store_order (id, created_at, payment_status, customer_id) values (894, '2023-11-06 10:47:54', 'F', 657);
                insert into store_order (id, created_at, payment_status, customer_id) values (895, '2023-07-25 09:48:44', 'C', 480);
                insert into store_order (id, created_at, payment_status, customer_id) values (896, '2023-08-25 23:21:55', 'F', 2);
                insert into store_order (id, created_at, payment_status, customer_id) values (897, '2023-09-14 04:41:16', 'C', 403);
                insert into store_order (id, created_at, payment_status, customer_id) values (898, '2023-01-01 12:18:03', 'F', 993);
                insert into store_order (id, created_at, payment_status, customer_id) values (899, '2023-12-06 23:48:02', 'C', 80);
                insert into store_order (id, created_at, payment_status, customer_id) values (900, '2023-06-17 02:17:24', 'P', 398);
                insert into store_order (id, created_at, payment_status, customer_id) values (901, '2022-09-12 15:24:58', 'P', 353);
                insert into store_order (id, created_at, payment_status, customer_id) values (902, '2023-01-21 17:36:18', 'P', 214);
                insert into store_order (id, created_at, payment_status, customer_id) values (903, '2024-01-04 17:28:21', 'P', 655);
                insert into store_order (id, created_at, payment_status, customer_id) values (904, '2023-08-13 07:38:35', 'P', 711);
                insert into store_order (id, created_at, payment_status, customer_id) values (905, '2024-06-23 20:18:59', 'F', 291);
                insert into store_order (id, created_at, payment_status, customer_id) values (906, '2024-03-11 02:01:44', 'F', 949);
                insert into store_order (id, created_at, payment_status, customer_id) values (907, '2023-03-26 06:47:54', 'P', 577);
                insert into store_order (id, created_at, payment_status, customer_id) values (908, '2024-04-05 10:39:18', 'P', 128);
                insert into store_order (id, created_at, payment_status, customer_id) values (909, '2023-01-11 02:12:03', 'P', 622);
                insert into store_order (id, created_at, payment_status, customer_id) values (910, '2023-09-30 21:40:31', 'C', 361);
                insert into store_order (id, created_at, payment_status, customer_id) values (911, '2023-01-16 01:29:36', 'P', 461);
                insert into store_order (id, created_at, payment_status, customer_id) values (912, '2024-02-02 13:55:50', 'F', 338);
                insert into store_order (id, created_at, payment_status, customer_id) values (913, '2022-09-28 15:19:02', 'C', 301);
                insert into store_order (id, created_at, payment_status, customer_id) values (914, '2023-10-14 00:02:41', 'P', 839);
                insert into store_order (id, created_at, payment_status, customer_id) values (915, '2022-07-09 02:36:51', 'F', 797);
                insert into store_order (id, created_at, payment_status, customer_id) values (916, '2023-01-16 14:35:54', 'P', 445);
                insert into store_order (id, created_at, payment_status, customer_id) values (917, '2022-10-05 01:51:36', 'C', 443);
                insert into store_order (id, created_at, payment_status, customer_id) values (918, '2024-07-05 08:53:50', 'P', 972);
                insert into store_order (id, created_at, payment_status, customer_id) values (919, '2023-05-25 03:23:27', 'F', 684);
                insert into store_order (id, created_at, payment_status, customer_id) values (920, '2023-06-19 15:45:34', 'F', 608);
                insert into store_order (id, created_at, payment_status, customer_id) values (921, '2022-09-17 00:40:22', 'F', 549);
                insert into store_order (id, created_at, payment_status, customer_id) values (922, '2023-08-08 12:29:12', 'P', 673);
                insert into store_order (id, created_at, payment_status, customer_id) values (923, '2022-10-20 02:55:00', 'F', 713);
                insert into store_order (id, created_at, payment_status, customer_id) values (924, '2023-10-24 15:39:58', 'P', 25);
                insert into store_order (id, created_at, payment_status, customer_id) values (925, '2024-05-24 09:41:44', 'F', 898);
                insert into store_order (id, created_at, payment_status, customer_id) values (926, '2022-11-23 11:39:36', 'F', 353);
                insert into store_order (id, created_at, payment_status, customer_id) values (927, '2023-07-15 14:53:56', 'C', 314);
                insert into store_order (id, created_at, payment_status, customer_id) values (928, '2023-06-24 23:53:47', 'C', 813);
                insert into store_order (id, created_at, payment_status, customer_id) values (929, '2022-08-16 00:55:20', 'C', 517);
                insert into store_order (id, created_at, payment_status, customer_id) values (930, '2023-07-01 09:46:43', 'P', 690);
                insert into store_order (id, created_at, payment_status, customer_id) values (931, '2022-12-05 15:41:53', 'P', 677);
                insert into store_order (id, created_at, payment_status, customer_id) values (932, '2023-07-22 06:35:27', 'P', 297);
                insert into store_order (id, created_at, payment_status, customer_id) values (933, '2022-08-07 10:57:58', 'C', 888);
                insert into store_order (id, created_at, payment_status, customer_id) values (934, '2024-05-14 18:20:04', 'P', 326);
                insert into store_order (id, created_at, payment_status, customer_id) values (935, '2022-11-20 10:36:02', 'C', 659);
                insert into store_order (id, created_at, payment_status, customer_id) values (936, '2023-10-17 05:32:01', 'P', 929);
                insert into store_order (id, created_at, payment_status, customer_id) values (937, '2022-10-09 02:09:51', 'P', 68);
                insert into store_order (id, created_at, payment_status, customer_id) values (938, '2023-05-16 03:51:42', 'P', 989);
                insert into store_order (id, created_at, payment_status, customer_id) values (939, '2023-02-28 19:55:17', 'F', 720);
                insert into store_order (id, created_at, payment_status, customer_id) values (940, '2023-05-04 05:25:54', 'C', 293);
                insert into store_order (id, created_at, payment_status, customer_id) values (941, '2024-04-03 09:31:49', 'P', 798);
                insert into store_order (id, created_at, payment_status, customer_id) values (942, '2023-08-04 15:12:51', 'F', 123);
                insert into store_order (id, created_at, payment_status, customer_id) values (943, '2022-11-22 17:47:01', 'F', 790);
                insert into store_order (id, created_at, payment_status, customer_id) values (944, '2023-05-30 05:53:25', 'P', 946);
                insert into store_order (id, created_at, payment_status, customer_id) values (945, '2024-01-30 17:48:59', 'C', 151);
                insert into store_order (id, created_at, payment_status, customer_id) values (946, '2024-06-13 01:58:44', 'F', 985);
                insert into store_order (id, created_at, payment_status, customer_id) values (947, '2023-08-30 17:45:18', 'P', 682);
                insert into store_order (id, created_at, payment_status, customer_id) values (948, '2022-12-07 14:11:38', 'C', 48);
                insert into store_order (id, created_at, payment_status, customer_id) values (949, '2023-02-08 00:30:37', 'F', 273);
                insert into store_order (id, created_at, payment_status, customer_id) values (950, '2024-02-29 23:54:54', 'P', 283);
                insert into store_order (id, created_at, payment_status, customer_id) values (951, '2023-11-26 19:44:12', 'C', 204);
                insert into store_order (id, created_at, payment_status, customer_id) values (952, '2024-03-21 05:35:55', 'P', 934);
                insert into store_order (id, created_at, payment_status, customer_id) values (953, '2022-12-27 03:04:25', 'F', 988);
                insert into store_order (id, created_at, payment_status, customer_id) values (954, '2023-08-30 02:18:58', 'P', 137);
                insert into store_order (id, created_at, payment_status, customer_id) values (955, '2024-05-04 02:48:47', 'C', 233);
                insert into store_order (id, created_at, payment_status, customer_id) values (956, '2023-01-31 20:43:59', 'F', 722);
                insert into store_order (id, created_at, payment_status, customer_id) values (957, '2023-01-26 00:24:47', 'F', 687);
                insert into store_order (id, created_at, payment_status, customer_id) values (958, '2023-09-20 02:51:51', 'C', 37);
                insert into store_order (id, created_at, payment_status, customer_id) values (959, '2023-04-14 17:09:17', 'P', 414);
                insert into store_order (id, created_at, payment_status, customer_id) values (960, '2023-11-22 15:42:52', 'F', 724);
                insert into store_order (id, created_at, payment_status, customer_id) values (961, '2023-01-23 15:36:09', 'C', 608);
                insert into store_order (id, created_at, payment_status, customer_id) values (962, '2024-04-08 06:46:21', 'F', 792);
                insert into store_order (id, created_at, payment_status, customer_id) values (963, '2023-08-22 01:15:42', 'C', 610);
                insert into store_order (id, created_at, payment_status, customer_id) values (964, '2023-01-05 23:40:36', 'C', 743);
                insert into store_order (id, created_at, payment_status, customer_id) values (965, '2023-10-11 08:20:55', 'F', 724);
                insert into store_order (id, created_at, payment_status, customer_id) values (966, '2023-01-02 00:52:47', 'C', 365);
                insert into store_order (id, created_at, payment_status, customer_id) values (967, '2023-07-19 11:07:01', 'C', 138);
                insert into store_order (id, created_at, payment_status, customer_id) values (968, '2022-10-19 00:21:54', 'P', 937);
                insert into store_order (id, created_at, payment_status, customer_id) values (969, '2024-05-08 22:31:51', 'P', 506);
                insert into store_order (id, created_at, payment_status, customer_id) values (970, '2023-10-10 19:43:11', 'P', 855);
                insert into store_order (id, created_at, payment_status, customer_id) values (971, '2024-05-23 05:20:20', 'F', 894);
                insert into store_order (id, created_at, payment_status, customer_id) values (972, '2023-11-03 09:00:12', 'F', 992);
                insert into store_order (id, created_at, payment_status, customer_id) values (973, '2024-01-18 18:32:21', 'F', 27);
                insert into store_order (id, created_at, payment_status, customer_id) values (974, '2024-06-10 20:48:22', 'F', 695);
                insert into store_order (id, created_at, payment_status, customer_id) values (975, '2024-02-15 05:53:02', 'C', 937);
                insert into store_order (id, created_at, payment_status, customer_id) values (976, '2022-10-20 01:06:41', 'C', 556);
                insert into store_order (id, created_at, payment_status, customer_id) values (977, '2024-03-06 17:27:29', 'C', 441);
                insert into store_order (id, created_at, payment_status, customer_id) values (978, '2023-10-20 13:05:44', 'F', 724);
                insert into store_order (id, created_at, payment_status, customer_id) values (979, '2023-08-02 06:13:54', 'P', 266);
                insert into store_order (id, created_at, payment_status, customer_id) values (980, '2023-10-10 07:06:22', 'F', 610);
                insert into store_order (id, created_at, payment_status, customer_id) values (981, '2024-06-15 00:31:32', 'P', 595);
                insert into store_order (id, created_at, payment_status, customer_id) values (982, '2023-06-15 11:29:15', 'P', 707);
                insert into store_order (id, created_at, payment_status, customer_id) values (983, '2024-02-04 22:44:22', 'P', 559);
                insert into store_order (id, created_at, payment_status, customer_id) values (984, '2023-06-01 21:41:32', 'F', 301);
                insert into store_order (id, created_at, payment_status, customer_id) values (985, '2024-04-07 18:50:32', 'C', 327);
                insert into store_order (id, created_at, payment_status, customer_id) values (986, '2023-03-01 12:06:32', 'C', 517);
                insert into store_order (id, created_at, payment_status, customer_id) values (987, '2023-05-21 11:05:27', 'F', 725);
                insert into store_order (id, created_at, payment_status, customer_id) values (988, '2023-02-18 06:56:53', 'C', 839);
                insert into store_order (id, created_at, payment_status, customer_id) values (989, '2024-07-01 21:32:40', 'P', 981);
                insert into store_order (id, created_at, payment_status, customer_id) values (990, '2022-07-20 00:27:40', 'C', 509);
                insert into store_order (id, created_at, payment_status, customer_id) values (991, '2022-12-17 06:38:43', 'F', 185);
                insert into store_order (id, created_at, payment_status, customer_id) values (992, '2023-12-15 01:08:46', 'F', 647);
                insert into store_order (id, created_at, payment_status, customer_id) values (993, '2024-02-25 01:11:48', 'P', 797);
                insert into store_order (id, created_at, payment_status, customer_id) values (994, '2023-12-23 07:39:54', 'F', 702);
                insert into store_order (id, created_at, payment_status, customer_id) values (995, '2023-01-12 11:40:02', 'F', 347);
                insert into store_order (id, created_at, payment_status, customer_id) values (996, '2022-12-27 07:32:45', 'P', 850);
                insert into store_order (id, created_at, payment_status, customer_id) values (997, '2022-08-14 09:05:48', 'F', 102);
                insert into store_order (id, created_at, payment_status, customer_id) values (998, '2024-01-07 16:43:07', 'P', 921);
                insert into store_order (id, created_at, payment_status, customer_id) values (999, '2023-02-17 09:40:48', 'P', 447);
                insert into store_order (id, created_at, payment_status, customer_id) values (1000, '2023-07-24 15:27:36', 'F', 435);
            ''',
            '''
                insert into store_orderitem (id, product_title, unit_price, quantity) values (1, 'Bagel - Everything Presliced', 61.19, 116);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (2, 'Mustard - Pommery', 16.75, 232);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (3, 'Pea - Snow', 83.86, 274);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (4, 'Tendrils - Baby Pea, Organic', 63.34, 100);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (5, 'Cheese - Cambozola', 54.62, 297);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (6, 'Coffee - Hazelnut Cream', 49.69, 47);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (7, 'Stock - Fish', 14.96, 289);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (8, 'V8 - Vegetable Cocktail', 6.8, 142);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (9, 'Corn - Mini', 7.51, 131);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (10, 'Cinnamon Rolls', 8.48, 54);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (11, 'Milk - Homo', 92.36, 225);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (12, 'Kumquat', 54.14, 83);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (13, 'Toothpick Frilled', 76.73, 299);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (14, 'Wine - Vouvray Cuvee Domaine', 2.21, 229);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (15, 'Filling - Mince Meat', 52.31, 44);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (16, 'Pepper - Cubanelle', 6.49, 172);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (17, 'Appetizer - Smoked Salmon / Dill', 10.27, 101);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (18, 'Coconut - Whole', 33.87, 106);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (19, 'Wine - Balbach Riverside', 5.24, 197);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (20, 'Tea - Lemon Green Tea', 27.57, 204);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (21, 'Mushroom - Portebello', 66.03, 139);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (22, 'Pear - Prickly', 91.2, 288);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (23, 'Pastry - Cheese Baked Scones', 34.74, 244);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (24, 'Sherry - Dry', 5.55, 215);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (25, 'Oil - Sunflower', 74.86, 23);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (26, 'Bread Crumbs - Japanese Style', 74.6, 59);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (27, 'Pastry - Banana Tea Loaf', 88.03, 141);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (28, 'Cheese - Fontina', 53.29, 294);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (29, 'Jolt Cola - Electric Blue', 46.51, 201);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (30, 'Fib N9 - Prague Powder', 13.15, 26);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (31, 'Beer - Upper Canada Light', 51.32, 268);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (32, 'Gingerale - Diet - Schweppes', 59.45, 86);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (33, 'Table Cloth 81x81 Colour', 72.87, 274);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (34, 'Chick Peas - Canned', 70.49, 66);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (35, 'Pur Value', 91.63, 6);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (36, 'Sugar - Monocystal / Rock', 92.25, 133);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (37, 'Garam Masala Powder', 30.26, 27);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (38, 'Beans - Wax', 11.27, 33);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (39, 'Mix - Cocktail Ice Cream', 51.42, 12);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (40, 'Cumin - Ground', 31.04, 21);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (41, 'Cheese - Woolwich Goat, Log', 63.27, 87);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (42, 'Wine - White, Colubia Cresh', 73.88, 286);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (43, 'The Pop Shoppe - Black Cherry', 25.2, 294);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (44, 'Veal - Tenderloin, Untrimmed', 39.66, 246);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (45, 'Tuna - Sushi Grade', 57.3, 85);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (46, 'Pepper - Chillies, Crushed', 82.97, 88);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (47, 'Salmon Atl.whole 8 - 10 Lb', 71.72, 249);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (48, 'Foam Espresso Cup Plain White', 97.5, 7);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (49, 'Veal - Inside Round / Top, Lean', 76.98, 74);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (50, 'Instant Coffee', 63.61, 66);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (51, 'Coffee - 10oz Cup 92961', 31.08, 71);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (52, 'Pail - 15l White, With Handle', 14.48, 190);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (53, 'Beans - Black Bean, Dry', 41.89, 171);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (54, 'Shortbread - Cookie Crumbs', 98.59, 134);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (55, 'Scallops - In Shell', 58.93, 4);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (56, 'Chicken Breast Wing On', 82.93, 9);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (57, 'Sole - Fillet', 74.27, 53);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (58, 'Icecream Bar - Del Monte', 27.62, 60);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (59, 'Sauce - Bernaise, Mix', 95.88, 59);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (60, 'Tortillas - Flour, 10', 50.68, 112);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (61, 'Butter Sweet', 42.67, 18);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (62, 'Brocolinni - Gaylan, Chinese', 31.54, 100);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (63, 'Cookie - Oreo 100x2', 14.53, 105);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (64, 'Seedlings - Clamshell', 26.92, 89);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (65, 'Wine - Ej Gallo Sierra Valley', 38.82, 296);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (66, 'Corn Meal', 20.51, 296);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (67, 'Squash - Sunburst', 88.41, 53);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (68, 'Chicken - Tenderloin', 64.11, 26);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (69, 'Asparagus - Green, Fresh', 87.23, 123);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (70, 'Cactus Pads', 46.92, 163);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (71, 'Eel - Smoked', 70.65, 296);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (72, 'Tray - 16in Rnd Blk', 71.89, 119);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (73, 'Wine - Magnotta - Bel Paese White', 5.83, 202);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (74, 'Wine - Ej Gallo Sierra Valley', 3.44, 165);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (75, 'Wine - Zonnebloem Pinotage', 78.52, 109);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (76, 'Flour - Cake', 54.38, 213);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (77, 'Radish', 83.25, 289);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (78, 'Veal - Nuckle', 94.89, 121);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (79, 'Coffee - Frthy Coffee Crisp', 64.61, 281);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (80, 'Pork - Ground', 21.86, 233);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (81, 'Peas Snow', 96.76, 294);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (82, 'Sloe Gin - Mcguinness', 44.4, 103);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (83, 'Pasta - Cappellini, Dry', 71.95, 201);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (84, 'Goulash Seasoning', 18.04, 231);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (85, 'Sour Puss - Tangerine', 30.48, 122);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (86, 'Sobe - Orange Carrot', 19.71, 242);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (87, 'Wine - White, Antinore Orvieto', 93.18, 120);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (88, 'Trueblue - Blueberry', 49.4, 16);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (89, 'Pernod', 81.79, 3);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (90, 'Cream - 35%', 46.85, 4);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (91, 'Muffin Carrot - Individual', 96.37, 222);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (92, 'Juice - Pineapple, 48 Oz', 61.47, 106);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (93, 'Hipnotiq Liquor', 80.54, 9);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (94, 'Soup - Verve - Chipotle Chicken', 98.54, 245);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (95, 'Instant Coffee', 97.25, 182);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (96, 'Tea Leaves - Oolong', 87.76, 1);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (97, 'Muffin Hinge - 211n', 79.29, 229);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (98, 'Veal - Liver', 12.56, 112);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (99, 'Grapefruit - Pink', 12.52, 127);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (100, 'Appetizer - Southwestern', 44.4, 295);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (101, 'Bagel - 12 Grain Preslice', 24.75, 86);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (102, 'Nut - Pecan, Pieces', 11.56, 274);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (103, 'Squash - Pattypan, Yellow', 42.72, 59);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (104, 'Currants', 3.15, 225);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (105, 'Numi - Assorted Teas', 48.92, 182);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (106, 'Wine - Winzer Krems Gruner', 39.89, 33);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (107, 'Sauce - Demi Glace', 88.18, 227);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (108, 'Eggplant Oriental', 87.53, 172);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (109, 'Chinese Foods - Chicken Wing', 81.53, 100);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (110, 'Coffee - Decafenated', 89.96, 99);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (111, 'Syrup - Monin, Irish Cream', 57.56, 239);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (112, 'Flour - Bread', 73.5, 130);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (113, 'Peach - Halves', 59.39, 145);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (114, 'Shopper Bag - S - 4', 62.81, 266);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (115, 'Sponge Cake Mix - Vanilla', 58.61, 154);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (116, 'Beef Tenderloin Aaa', 69.13, 234);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (117, 'Bacardi Limon', 89.94, 115);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (118, 'Soup - Beef, Base Mix', 63.02, 150);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (119, 'Vodka - Hot, Lnferno', 52.98, 224);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (120, 'Paper - Brown Paper Mini Cups', 16.91, 103);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (121, 'Tomatoes - Grape', 10.44, 298);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (122, 'Juice - Lime', 91.86, 184);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (123, 'Cake - Lemon Chiffon', 56.61, 93);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (124, 'Energy Drink', 86.23, 257);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (125, 'Tea - Earl Grey', 8.85, 47);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (126, 'Longos - Burritos', 53.79, 87);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (127, 'Straw - Regular', 82.73, 65);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (128, 'Foam Tray S2', 44.02, 146);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (129, 'Wine - Sauvignon Blanc Oyster', 94.22, 31);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (130, 'Onions - Red Pearl', 65.53, 201);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (131, 'Egg - Salad Premix', 67.56, 284);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (132, 'Venison - Denver Leg Boneless', 38.65, 49);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (133, 'Beets - Candy Cane, Organic', 33.62, 280);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (134, 'Lettuce - Curly Endive', 17.69, 28);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (135, 'Tomatoes', 47.21, 226);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (136, 'Extract Vanilla Pure', 27.98, 270);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (137, 'Beef - Short Ribs', 7.97, 19);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (138, 'Nantucket - Orange Mango Cktl', 6.09, 280);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (139, 'Beer - Camerons Auburn', 5.0, 138);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (140, 'Bandage - Fexible 1x3', 28.58, 102);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (141, 'Chivas Regal - 12 Year Old', 68.5, 24);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (142, 'Squid U5 - Thailand', 45.84, 237);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (143, 'Ostrich - Fan Fillet', 27.73, 170);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (144, 'Nestea - Ice Tea, Diet', 74.31, 109);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (145, 'Sauce - Soya, Dark', 15.34, 230);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (146, 'Flour - Chickpea', 46.78, 251);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (147, 'Sauce Tomato Pouch', 85.56, 297);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (148, 'Butter - Pod', 55.33, 111);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (149, 'Syrup - Monin, Swiss Choclate', 96.43, 117);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (150, 'Greens Mustard', 96.96, 291);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (151, 'White Baguette', 27.21, 39);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (152, 'Grapes - Red', 22.95, 72);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (153, 'Red Snapper - Fillet, Skin On', 7.2, 108);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (154, 'Molasses - Fancy', 85.55, 82);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (155, 'Truffle - Whole Black Peeled', 87.31, 108);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (156, 'Slt - Individual Portions', 1.68, 260);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (157, 'Scotch - Queen Anne', 88.12, 143);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (158, 'Spinach - Frozen', 10.91, 237);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (159, 'Soup - Campbells, Classic Chix', 17.33, 57);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (160, 'Ham - Virginia', 33.26, 105);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (161, 'Galliano', 9.42, 120);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (162, 'Dish Towel', 81.33, 61);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (163, 'Jicama', 18.92, 11);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (164, 'Melon - Honey Dew', 72.45, 44);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (165, 'Grapefruit - White', 10.7, 123);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (166, 'Dill - Primerba, Paste', 40.59, 206);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (167, 'Pork - Chop, Frenched', 25.62, 206);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (168, 'Olives - Green, Pitted', 6.57, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (169, 'Versatainer Nc - 888', 12.46, 73);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (170, 'Egg - Salad Premix', 66.85, 95);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (171, 'Beef - Montreal Smoked Brisket', 6.75, 238);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (172, 'Lamb - Whole Head Off,nz', 16.42, 149);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (173, 'Sprouts - Alfalfa', 49.22, 202);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (174, 'Molasses - Fancy', 27.49, 255);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (175, 'Whmis Spray Bottle Graduated', 4.66, 96);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (176, 'Pastry - Cheese Baked Scones', 19.15, 74);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (177, 'Watercress', 92.04, 233);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (178, 'Beef - Tenderloin Tails', 72.38, 181);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (179, 'Pur Value', 79.12, 154);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (180, 'Otomegusa Dashi Konbu', 77.28, 190);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (181, 'Wiberg Cure', 53.31, 256);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (182, 'Nantucket Orange Juice', 74.65, 126);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (183, 'Vinegar - Sherry', 15.2, 138);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (184, 'Flower - Daisies', 17.19, 179);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (185, 'Vaccum Bag 10x13', 24.41, 240);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (186, 'Lamb - Racks, Frenched', 1.16, 50);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (187, 'Wine - Conde De Valdemar', 50.01, 272);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (188, 'Wine - Valpolicella Masi', 14.45, 194);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (189, 'Steam Pan - Half Size Deep', 57.31, 237);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (190, 'Mince Meat - Filling', 98.2, 78);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (191, 'Wine - Malbec Trapiche Reserve', 31.51, 226);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (192, 'Cinnamon - Stick', 66.08, 98);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (193, 'Trueblue - Blueberry 12x473ml', 62.17, 43);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (194, 'Wine - Coteaux Du Tricastin Ac', 20.89, 148);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (195, 'Silicone Parch. 16.3x24.3', 84.61, 178);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (196, 'Dried Cherries', 37.38, 142);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (197, 'Compound - Raspberry', 6.07, 186);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (198, 'Parsley - Dried', 86.44, 51);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (199, 'Bread - 10 Grain Parisian', 66.01, 122);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (200, 'The Pop Shoppe Pinapple', 90.68, 244);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (201, 'Garlic Powder', 29.62, 224);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (202, 'Irish Cream - Baileys', 80.2, 155);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (203, 'Wine - Barbera Alba Doc 2001', 20.55, 181);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (204, 'Sea Bass - Fillets', 91.07, 55);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (205, 'Bread Country Roll', 61.35, 299);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (206, 'Asparagus - Green, Fresh', 19.03, 140);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (207, 'Berry Brulee', 40.97, 204);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (208, 'Mushroom - Portebello', 61.69, 57);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (209, 'Grand Marnier', 81.98, 105);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (210, 'Tomatoes - Plum, Canned', 50.34, 198);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (211, 'Cake - Lemon Chiffon', 68.89, 42);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (212, 'Pesto - Primerba, Paste', 47.75, 94);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (213, 'Glass - Wine, Plastic, Clear 5 Oz', 73.29, 297);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (214, 'Celery', 51.04, 156);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (215, 'Chips Potato Salt Vinegar 43g', 42.95, 90);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (216, 'Pate - Peppercorn', 98.47, 104);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (217, 'Cake - Bande Of Fruit', 58.07, 250);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (218, 'Pepper - Jalapeno', 63.29, 233);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (219, 'Lamb - Leg, Diced', 30.06, 136);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (220, 'Beer - Sleeman Fine Porter', 19.11, 13);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (221, 'Cheese - Gouda', 45.7, 200);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (222, 'Muffin Mix - Chocolate Chip', 87.94, 30);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (223, 'Olives - Stuffed', 21.61, 89);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (224, 'Ostrich - Prime Cut', 70.02, 209);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (225, 'Paper - Brown Paper Mini Cups', 65.28, 147);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (226, 'Assorted Desserts', 64.35, 140);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (227, 'Squeeze Bottle', 81.3, 250);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (228, 'Pepper - Paprika, Hungarian', 18.82, 83);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (229, 'Spice - Peppercorn Melange', 36.0, 260);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (230, 'Southern Comfort', 13.56, 36);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (231, 'Port - 74 Brights', 35.42, 224);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (232, 'Chicken - Livers', 78.82, 144);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (233, 'Wine - Red, Mosaic Zweigelt', 42.09, 205);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (234, 'Creme De Banane - Marie', 81.88, 137);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (235, 'Shrimp, Dried, Small / Lb', 29.97, 96);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (236, 'Hold Up Tool Storage Rack', 76.78, 193);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (237, 'Crab Meat Claw Pasteurise', 96.66, 91);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (238, 'Nestea - Ice Tea, Diet', 9.14, 172);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (239, 'Towels - Paper / Kraft', 57.75, 203);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (240, 'Bread - Burger', 92.93, 294);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (241, 'Bread - Pain Au Liat X12', 14.91, 202);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (242, 'Sauce - Demi Glace', 63.05, 95);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (243, 'Kiwi Gold Zespri', 72.46, 57);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (244, 'Soup - Campbells, Minestrone', 5.27, 154);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (245, 'Chives - Fresh', 91.56, 182);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (246, 'Bread - Crusty Italian Poly', 58.23, 165);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (247, 'Chicken - White Meat, No Tender', 92.44, 172);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (248, 'Cheese - Augre Des Champs', 58.53, 268);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (249, 'Truffle Paste', 28.43, 43);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (250, 'Melon - Watermelon, Seedless', 40.56, 128);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (251, 'Tomatoes - Grape', 40.64, 202);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (252, 'Wine - Hardys Bankside Shiraz', 78.32, 59);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (253, 'Rum - Spiced, Captain Morgan', 55.71, 163);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (254, 'Crackers - Soda / Saltins', 3.69, 61);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (255, 'Cake Circle, Foil, Scallop', 90.69, 141);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (256, 'Wine - Harrow Estates, Vidal', 89.65, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (257, 'Tilapia - Fillets', 72.27, 150);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (258, 'Lentils - Green, Dry', 24.02, 226);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (259, 'Cookie Choc', 83.55, 169);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (260, 'Beans - Black Bean, Canned', 25.64, 31);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (261, 'Oranges - Navel, 72', 41.84, 276);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (262, 'Cheese - Swiss Sliced', 96.29, 183);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (263, 'Turkey - Breast, Double', 21.89, 286);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (264, 'Sausage - Blood Pudding', 63.86, 299);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (265, 'Cranberries - Fresh', 35.27, 261);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (266, 'Chicken - Leg, Boneless', 54.49, 227);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (267, 'Cranberry Foccacia', 17.73, 217);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (268, 'Rice - Sushi', 23.99, 34);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (269, 'Table Cloth 81x81 White', 44.64, 58);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (270, 'Bread - Pumpernickle, Rounds', 83.26, 231);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (271, 'Beef - Texas Style Burger', 27.79, 200);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (272, 'Rum - Dark, Bacardi, Black', 21.41, 102);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (273, 'Olives - Nicoise', 12.74, 10);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (274, 'Wine - Rosso Del Veronese Igt', 11.34, 205);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (275, 'Extract - Almond', 74.8, 290);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (276, 'Wine - Red, Mouton Cadet', 67.06, 168);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (277, 'Sugar - Fine', 98.14, 270);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (278, 'Tomatoes - Cherry, Yellow', 89.25, 13);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (279, 'Bread - Burger', 6.86, 221);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (280, 'Lettuce - Treviso', 41.98, 239);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (281, 'Wine - Magnotta, White', 28.15, 289);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (282, 'Soup - Campbells Chili Veg', 68.55, 237);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (283, 'Ginger - Pickled', 68.92, 54);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (284, 'Wine - Coteaux Du Tricastin Ac', 54.61, 215);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (285, 'Snapple Lemon Tea', 51.97, 160);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (286, 'Drambuie', 78.29, 47);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (287, 'Ice Cream Bar - Hagen Daz', 2.46, 13);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (288, 'Cheese - Boursin, Garlic / Herbs', 30.96, 283);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (289, 'Cake - Mini Cheesecake', 13.93, 93);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (290, 'Apron', 31.17, 91);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (291, 'Scallops - 20/30', 77.35, 204);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (292, 'Wine - Chenin Blanc K.w.v.', 55.11, 132);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (293, 'Tart Shells - Barquettes, Savory', 79.82, 146);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (294, 'Wine - Peller Estates Late', 20.35, 257);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (295, 'Chocolate - Feathers', 6.07, 20);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (296, 'Curry Paste - Madras', 56.99, 297);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (297, 'Flour - Chickpea', 23.76, 300);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (298, 'Bandage - Fexible 1x3', 25.01, 102);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (299, 'Wine - Fume Blanc Fetzer', 68.69, 68);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (300, 'Shiro Miso', 36.77, 50);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (301, 'Tea Peppermint', 23.49, 273);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (302, 'Wine La Vielle Ferme Cote Du', 2.64, 35);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (303, 'Pernod', 17.17, 225);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (304, 'Lamb - Racks, Frenched', 37.34, 250);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (305, 'Skewers - Bamboo', 51.01, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (306, 'Lobster - Tail 6 Oz', 74.55, 172);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (307, 'Wine - Semi Dry Riesling Vineland', 54.1, 275);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (308, 'Cheese - Marble', 1.19, 46);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (309, 'Wine - Wyndham Estate Bin 777', 80.76, 97);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (310, 'Wine - Remy Pannier Rose', 34.37, 275);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (311, 'Wine - Bourgogne 2002, La', 22.0, 248);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (312, 'Melon - Watermelon Yellow', 97.64, 119);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (313, 'Soup - Campbells, Classic Chix', 33.11, 101);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (314, 'Sage Ground Wiberg', 71.39, 158);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (315, 'Sponge Cake Mix - Vanilla', 91.99, 73);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (316, 'Chicken - White Meat With Tender', 80.66, 130);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (317, 'Split Peas - Green, Dry', 2.97, 196);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (318, 'Table Cloth 54x72 Colour', 66.27, 143);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (319, 'Ecolab - Solid Fusion', 18.74, 151);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (320, 'Soup - French Can Pea', 7.1, 16);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (321, 'Soho Lychee Liqueur', 64.87, 202);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (322, 'Wild Boar - Tenderloin', 57.97, 104);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (323, 'Broom - Push', 99.02, 107);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (324, 'Extract - Lemon', 61.22, 58);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (325, 'Energy Drink - Franks Pineapple', 65.08, 20);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (326, 'Puree - Blackcurrant', 71.17, 135);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (327, 'Gatorade - Orange', 70.18, 272);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (328, 'Hot Chocolate - Individual', 39.91, 24);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (329, 'Tea - Herbal - 6 Asst', 58.89, 277);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (330, 'Napkin - Beverage 1 Ply', 3.71, 146);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (331, 'Cheese - Brick With Pepper', 75.18, 131);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (332, 'Pate - Peppercorn', 93.22, 86);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (333, 'Sobe - Lizard Fuel', 63.73, 300);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (334, 'Versatainer Nc - 9388', 79.13, 86);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (335, 'Lettuce - Mini Greens, Whole', 34.83, 223);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (336, 'Table Cloth 90x90 White', 19.35, 27);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (337, 'Cookie Double Choco', 68.09, 266);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (338, 'Icecream Bar - Del Monte', 5.93, 131);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (339, 'Wine - White, Cooking', 10.72, 25);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (340, 'Rice - Basmati', 29.27, 292);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (341, 'Juice - Cranberry 284ml', 92.79, 106);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (342, 'Apricots - Dried', 8.37, 133);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (343, 'Muffin Mix - Lemon Cranberry', 94.62, 142);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (344, 'Spinach - Frozen', 28.88, 107);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (345, 'Wine - Two Oceans Cabernet', 27.48, 128);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (346, 'Pears - Fiorelle', 22.42, 291);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (347, 'Pail With Metal Handle 16l White', 92.0, 36);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (348, 'Versatainer Nc - 8288', 64.25, 1);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (349, 'Longos - Chicken Cordon Bleu', 5.38, 202);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (350, 'Wine - Red, Wolf Blass, Yellow', 1.89, 205);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (351, 'Baking Soda', 38.02, 19);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (352, 'Bacardi Breezer - Strawberry', 64.96, 99);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (353, 'Sorrel - Fresh', 84.82, 116);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (354, 'Gooseberry', 38.86, 130);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (355, 'Gherkin - Sour', 21.87, 129);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (356, 'Chicken - Livers', 68.35, 30);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (357, 'Cookies - Assorted', 71.63, 178);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (358, 'Garlic Powder', 78.32, 108);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (359, 'Bread - Roll, Calabrese', 88.06, 17);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (360, 'Soap - Hand Soap', 95.89, 167);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (361, 'Breakfast Quesadillas', 67.94, 239);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (362, 'Broom Handle', 44.16, 40);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (363, 'Pheasants - Whole', 98.79, 233);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (364, 'Lobak', 69.2, 76);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (365, 'Godiva White Chocolate', 91.75, 125);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (366, 'Beef - Rib Roast, Cap On', 89.46, 277);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (367, 'Calvados - Boulard', 78.89, 269);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (368, 'Coffee - Egg Nog Capuccino', 73.38, 86);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (369, 'Bacardi Mojito', 74.54, 267);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (370, 'Rum - Dark, Bacardi, Black', 56.12, 4);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (371, 'Goldschalger', 54.94, 165);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (372, 'Fondant - Icing', 25.51, 35);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (373, 'Juice - Prune', 18.43, 182);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (374, 'Coffee - French Vanilla Frothy', 77.86, 51);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (375, 'Sobe - Lizard Fuel', 46.09, 136);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (376, 'Loquat', 19.13, 42);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (377, 'Wine - Clavet Saint Emilion', 49.16, 195);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (378, 'Avocado', 15.39, 15);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (379, 'Oil - Food, Lacquer Spray', 47.64, 229);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (380, 'Ecolab - Power Fusion', 32.43, 1);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (381, 'Shrimp - 16 - 20 Cooked, Peeled', 25.01, 15);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (382, 'Peach - Halves', 83.01, 67);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (383, 'Wine - Gato Negro Cabernet', 12.92, 274);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (384, 'Spinach - Packaged', 2.54, 147);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (385, 'Remy Red', 92.22, 131);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (386, 'Table Cloth 54x72 Colour', 63.98, 217);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (387, 'Smirnoff Green Apple Twist', 79.3, 153);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (388, 'Arctic Char - Fresh, Whole', 31.87, 57);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (389, 'Lettuce Romaine Chopped', 97.03, 92);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (390, 'Salt - Sea', 74.87, 216);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (391, 'Placemat - Scallop, White', 63.31, 227);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (392, 'Carrots - Jumbo', 87.32, 283);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (393, 'Chocolate - Compound Coating', 82.91, 229);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (394, 'Pork - Bones', 39.39, 284);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (395, 'Bread - White Mini Epi', 97.0, 19);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (396, 'Vermacelli - Sprinkles, Assorted', 86.98, 147);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (397, 'Creamers - 10%', 36.14, 197);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (398, 'Pie Pecan', 28.49, 136);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (399, 'Veal - Leg', 48.58, 279);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (400, 'Wine - Alicanca Vinho Verde', 15.67, 291);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (401, 'Sauce - Rosee', 43.45, 83);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (402, 'Cherries - Fresh', 51.86, 22);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (403, 'Schnappes - Peach, Walkers', 19.8, 294);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (404, 'Gloves - Goldtouch Disposable', 2.19, 238);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (405, 'Lemon Pepper', 93.51, 161);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (406, 'Onions - Red Pearl', 27.74, 46);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (407, 'Juice - Apple, 1.36l', 85.59, 121);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (408, 'Wine - Magnotta - Bel Paese White', 5.01, 90);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (409, 'Appetizer - Lobster Phyllo Roll', 47.03, 16);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (410, 'Beef Wellington', 98.65, 197);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (411, 'Cheese - Mascarpone', 20.61, 76);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (412, 'Spice - Peppercorn Melange', 11.52, 156);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (413, 'Bar Mix - Lime', 84.03, 55);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (414, 'Monkfish - Fresh', 14.2, 29);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (415, 'Crab - Dungeness, Whole, live', 77.01, 227);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (416, 'Campari', 61.02, 41);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (417, 'Veal - Provimi Inside', 27.46, 9);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (418, 'Fish - Atlantic Salmon, Cold', 2.86, 110);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (419, 'Icecream - Dibs', 24.43, 270);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (420, 'Dried Figs', 51.81, 235);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (421, 'Chicken - Livers', 21.68, 198);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (422, 'Foil Wrap', 76.26, 226);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (423, 'Pasta - Elbows, Macaroni, Dry', 27.33, 93);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (424, 'Coffee - Almond Amaretto', 9.36, 162);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (425, 'Sprouts - Peppercress', 18.6, 78);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (426, 'Versatainer Nc - 888', 14.78, 193);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (427, 'Cookies - Fortune', 2.82, 273);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (428, 'Cheese - Mozzarella', 44.91, 127);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (429, 'Beef - Eye Of Round', 61.21, 268);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (430, 'Peach - Halves', 58.02, 204);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (431, 'Roe - Lump Fish, Black', 98.16, 72);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (432, 'Numi - Assorted Teas', 5.53, 80);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (433, 'Dc - Frozen Momji', 61.82, 243);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (434, 'Kiwi', 25.68, 128);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (435, 'Milk - Skim', 42.66, 127);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (436, 'Pork Ham Prager', 76.35, 53);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (437, 'Pork - Ham Hocks - Smoked', 17.42, 73);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (438, 'Kellogs All Bran Bars', 12.96, 199);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (439, 'Fireball Whisky', 6.11, 56);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (440, 'Wine - White, Riesling, Henry Of', 76.53, 83);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (441, 'Bouq All Italian - Primerba', 27.86, 246);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (442, 'Nut - Almond, Blanched, Ground', 12.8, 108);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (443, 'Vermouth - White, Cinzano', 62.16, 49);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (444, 'Hinge W Undercut', 93.55, 115);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (445, 'Water - Evian 355 Ml', 17.02, 200);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (446, 'Chicken - Breast, 5 - 7 Oz', 88.38, 111);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (447, 'Jameson Irish Whiskey', 96.01, 209);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (448, 'Wine - Sake', 34.65, 74);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (449, 'Jack Daniels', 90.91, 286);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (450, 'Tamarind Paste', 16.54, 138);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (451, 'Pastry - Chocolate Marble Tea', 44.35, 16);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (452, 'Eggroll', 45.58, 141);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (453, 'Tart Shells - Sweet, 4', 62.89, 133);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (454, 'Oregano - Fresh', 42.06, 114);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (455, 'Blackberries', 98.78, 245);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (456, 'Salmon Steak - Cohoe 6 Oz', 43.74, 169);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (457, 'Oneshot Automatic Soap System', 4.82, 240);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (458, 'Soup - Campbells Beef Noodle', 96.82, 212);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (459, 'Flour Pastry Super Fine', 48.38, 64);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (460, 'Soup - Campbells, Beef Barley', 26.54, 163);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (461, 'Puff Pastry - Sheets', 31.19, 92);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (462, 'Cheese - St. Paulin', 35.85, 138);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (463, 'Wine - Magnotta - Pinot Gris Sr', 39.37, 40);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (464, 'Wine - Savigny - Les - Beaune', 2.45, 136);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (465, 'Oil - Canola', 96.63, 199);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (466, 'Cup - Paper 10oz 92959', 78.07, 42);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (467, 'Beef - Top Sirloin - Aaa', 57.3, 204);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (468, 'Mangoes', 94.56, 3);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (469, 'Wine - Port Late Bottled Vintage', 89.43, 263);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (470, 'Cheese - Parmesan Cubes', 17.21, 139);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (471, 'Flower - Commercial Spider', 99.67, 42);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (472, 'Wine - White, Schroder And Schyl', 27.13, 89);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (473, 'Pork Salted Bellies', 90.62, 25);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (474, 'Truffle Cups Green', 27.49, 230);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (475, 'Wine - Rosso Toscano Igt', 27.64, 158);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (476, 'Mushroom - Shitake, Fresh', 27.13, 12);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (477, 'Dawn Professionl Pot And Pan', 84.51, 227);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (478, 'Shrimp - 100 / 200 Cold Water', 99.69, 107);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (479, 'Apple - Northern Spy', 42.98, 245);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (480, 'Pepper - Black, Whole', 63.86, 27);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (481, 'Ice Cream - Chocolate', 45.68, 245);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (482, 'Halibut - Fletches', 27.27, 51);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (483, 'Longos - Burritos', 84.43, 85);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (484, 'Vanilla Beans', 63.17, 233);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (485, 'Bread - Raisin Walnut Pull', 39.96, 18);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (486, 'Broom - Corn', 78.8, 9);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (487, 'Plasticknivesblack', 74.34, 76);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (488, 'V8 Pet', 30.97, 176);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (489, 'Versatainer Nc - 888', 70.58, 245);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (490, 'Horseradish - Prepared', 78.17, 165);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (491, 'Sauce - Apple, Unsweetened', 39.47, 271);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (492, 'Mcguinness - Blue Curacao', 71.4, 36);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (493, 'Flour - Strong', 13.95, 91);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (494, 'Carbonated Water - Blackberry', 11.77, 98);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (495, 'Soup Campbells Split Pea And Ham', 9.44, 195);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (496, 'Numi - Assorted Teas', 88.9, 138);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (497, 'Lamb - Loin Chops', 58.63, 37);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (498, 'Remy Red', 81.86, 118);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (499, 'Juice - Mango', 15.2, 175);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (500, 'Sping Loaded Cup Dispenser', 65.66, 294);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (501, 'Tray - Foam, Square 4 - S', 82.23, 90);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (502, 'Wine - Chianti Classica Docg', 56.63, 277);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (503, 'Cloves - Ground', 25.83, 146);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (504, 'Trueblue - Blueberry 12x473ml', 10.03, 227);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (505, 'Blueberries', 51.47, 75);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (506, 'Muffin Mix - Lemon Cranberry', 51.05, 187);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (507, 'Ice Cream - Life Savers', 23.25, 248);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (508, 'Olives - Green, Pitted', 14.98, 252);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (509, 'Beef - Top Butt', 8.62, 121);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (510, 'Broccoli - Fresh', 43.31, 136);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (511, 'Nut - Walnut, Pieces', 3.86, 260);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (512, 'Basil - Seedlings Cookstown', 89.45, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (513, 'Kiwi Gold Zespri', 2.82, 109);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (514, 'Water - Spring 1.5lit', 89.98, 209);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (515, 'Wine - Alicanca Vinho Verde', 7.48, 19);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (516, 'Pop Shoppe Cream Soda', 48.19, 6);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (517, 'Pepper - Roasted Red', 29.19, 267);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (518, 'Southern Comfort', 39.11, 241);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (519, 'Toothpick Frilled', 6.86, 170);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (520, 'Chicken - Breast, 5 - 7 Oz', 80.57, 246);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (521, 'Loaf Pan - 2 Lb, Foil', 81.75, 237);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (522, 'Wine - Kwv Chenin Blanc South', 81.94, 218);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (523, 'Chicken - Ground', 52.62, 66);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (524, 'Rabbit - Frozen', 6.46, 150);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (525, 'Chickhen - Chicken Phyllo', 92.8, 49);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (526, 'Cinnamon - Ground', 20.66, 242);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (527, 'Wine - White, Concha Y Toro', 60.99, 139);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (528, 'Creme De Cacao White', 92.72, 245);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (529, 'Peppercorns - Pink', 22.96, 290);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (530, 'Extract - Rum', 62.17, 27);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (531, 'Ice Cream - Strawberry', 18.51, 288);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (532, 'Tomato Puree', 1.11, 64);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (533, 'Apple - Granny Smith', 31.61, 7);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (534, 'Glass - Juice Clear 5oz 55005', 66.79, 127);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (535, 'Fond - Chocolate', 75.34, 274);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (536, 'Rum - Mount Gay Eclipes', 42.81, 281);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (537, 'Truffle Shells - White Chocolate', 94.64, 41);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (538, 'Beef Wellington', 24.03, 52);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (539, 'Flax Seed', 90.02, 233);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (540, 'Bread - French Baquette', 21.23, 191);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (541, 'Sugar - Icing', 57.74, 171);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (542, 'Sauce - Demi Glace', 17.2, 58);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (543, 'Lobster - Live', 7.82, 68);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (544, 'Soup Campbells Turkey Veg.', 39.62, 92);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (545, 'Yukon Jack', 30.84, 2);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (546, 'Cookie - Oreo 100x2', 51.95, 199);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (547, 'Glass - Wine, Plastic, Clear 5 Oz', 32.59, 107);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (548, 'Tea - English Breakfast', 92.81, 220);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (549, 'Syrup - Kahlua Chocolate', 33.88, 43);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (550, 'Pasta - Lasagne, Fresh', 36.39, 7);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (551, 'Coke - Classic, 355 Ml', 72.88, 120);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (552, 'Nut - Walnut, Chopped', 94.24, 118);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (553, 'Red Snapper - Fillet, Skin On', 20.74, 159);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (554, 'Beef - Roasted, Cooked', 50.0, 221);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (555, 'Sauce - Bernaise, Mix', 41.11, 217);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (556, 'Soup - Campbells, Cream Of', 78.96, 58);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (557, 'Chocolate - Semi Sweet', 3.04, 104);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (558, 'Ecolab - Hand Soap Form Antibac', 39.31, 146);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (559, 'Corn - Mini', 20.3, 229);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (560, 'Potato - Sweet', 95.67, 154);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (561, 'Fork - Plastic', 68.02, 12);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (562, 'Corn Meal', 80.44, 79);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (563, 'Yoplait - Strawbrasp Peac', 17.48, 276);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (564, 'Cheese - Goat With Herbs', 93.64, 174);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (565, 'Wine - Savigny - Les - Beaune', 35.32, 78);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (566, 'Veal Inside - Provimi', 68.07, 288);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (567, 'Sugar - Monocystal / Rock', 73.72, 148);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (568, 'Sauce - Cranberry', 93.61, 110);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (569, 'Apple - Fuji', 55.24, 86);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (570, 'Sole - Iqf', 93.75, 147);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (571, 'Chips - Doritos', 48.77, 262);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (572, 'Foam Espresso Cup Plain White', 88.56, 151);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (573, 'Crackers - Soda / Saltins', 68.32, 278);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (574, 'Pepper - Chipotle, Canned', 27.61, 1);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (575, 'Pork - Loin, Boneless', 28.64, 199);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (576, 'Island Oasis - Wildberry', 68.49, 234);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (577, 'Wine - Casillero Deldiablo', 46.61, 12);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (578, 'Pie Box - Cello Window 2.5', 88.34, 263);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (579, 'Anchovy In Oil', 64.97, 231);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (580, 'Sauce - Hp', 70.06, 190);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (581, 'Capers - Pickled', 56.04, 59);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (582, 'Wine - Gato Negro Cabernet', 43.73, 117);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (583, 'French Kiss Vanilla', 20.23, 51);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (584, 'Blackberries', 22.21, 232);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (585, 'Jagermeister', 50.67, 249);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (586, 'Beets - Pickled', 10.02, 296);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (587, 'Beer - Camerons Cream Ale', 7.43, 5);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (588, 'Devonshire Cream', 96.9, 117);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (589, 'Extract Vanilla Pure', 63.85, 55);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (590, 'Spice - Chili Powder Mexican', 9.51, 16);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (591, 'Lambcasing', 87.79, 177);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (592, 'Sprite - 355 Ml', 4.52, 186);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (593, 'Squid - Breaded', 47.82, 170);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (594, 'Veal - Heart', 62.07, 242);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (595, 'Snapple - Iced Tea Peach', 40.03, 211);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (596, 'Pastry - Raisin Muffin - Mini', 68.88, 65);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (597, 'Pepper - Paprika, Hungarian', 98.92, 287);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (598, 'Cup - 8oz Coffee Perforated', 36.65, 73);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (599, 'Broom - Corn', 52.1, 293);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (600, 'Rice - Brown', 66.88, 240);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (601, 'Sauce - Vodka Blush', 75.25, 113);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (602, 'Cookies - Amaretto', 78.92, 130);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (603, 'Ocean Spray - Ruby Red', 50.65, 151);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (604, 'Water - Aquafina Vitamin', 23.72, 147);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (605, 'Sour Puss Raspberry', 70.66, 84);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (606, 'Pastry - Lemon Danish - Mini', 40.97, 149);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (607, 'Pastry - Carrot Muffin - Mini', 39.84, 153);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (608, 'Curry Paste - Green Masala', 33.52, 60);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (609, 'Mustard - Dijon', 59.85, 69);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (610, 'Wooden Mop Handle', 80.15, 257);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (611, 'Evaporated Milk - Skim', 18.12, 53);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (612, 'Carbonated Water - Raspberry', 92.26, 185);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (613, 'Tea - Earl Grey', 28.86, 208);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (614, 'Wine - Magnotta - Belpaese', 30.5, 298);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (615, 'Pickerel - Fillets', 47.76, 123);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (616, 'General Purpose Trigger', 25.59, 275);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (617, 'Tortillas - Flour, 12', 15.78, 278);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (618, 'Soup - Campbells, Creamy', 58.12, 250);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (619, 'Pepper - Red Chili', 77.27, 82);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (620, 'Creme De Menth - White', 69.93, 214);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (621, 'Jerusalem Artichoke', 65.88, 229);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (622, 'Lettuce - Lolla Rosa', 65.28, 15);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (623, 'Langers - Cranberry Cocktail', 16.58, 77);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (624, 'Spinach - Spinach Leaf', 61.58, 124);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (625, 'Snails - Large Canned', 5.34, 192);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (626, 'Lamb Shoulder Boneless Nz', 50.39, 221);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (627, 'Ham - Cooked Italian', 27.87, 50);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (628, 'Macaroons - Homestyle Two Bit', 81.07, 144);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (629, 'Salmon - Atlantic, No Skin', 22.3, 133);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (630, 'Pineapple - Regular', 76.86, 184);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (631, 'Cornstarch', 88.41, 114);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (632, 'Filling - Mince Meat', 1.18, 61);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (633, 'Tarts Assorted', 83.21, 262);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (634, 'Water - San Pellegrino', 55.75, 106);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (635, 'Pasta - Fettuccine, Dry', 93.44, 5);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (636, 'Cheese - Gorgonzola', 16.94, 236);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (637, 'Melon - Watermelon Yellow', 72.71, 21);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (638, 'Bar Mix - Lemon', 25.1, 246);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (639, 'Bread - Sour Sticks With Onion', 87.14, 277);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (640, 'Bread - Rolls, Corn', 34.54, 94);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (641, 'Wine - Remy Pannier Rose', 34.76, 40);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (642, 'Cookies - Assorted', 82.58, 277);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (643, 'Squid - U - 10 Thailand', 35.7, 157);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (644, 'Water - Spring Water 500ml', 58.63, 273);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (645, 'Pork - Side Ribs', 9.25, 180);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (646, 'Dried Apple', 85.86, 283);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (647, 'Chinese Foods - Cantonese', 50.49, 162);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (648, 'Sauce - Oyster', 17.61, 93);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (649, 'Bread - 10 Grain', 32.26, 235);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (650, 'Vinegar - Champagne', 30.31, 269);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (651, 'Bread - Pita', 10.52, 194);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (652, 'Tea - Darjeeling, Azzura', 79.11, 134);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (653, 'Amarula Cream', 17.49, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (654, 'Containter - 3oz Microwave Rect.', 88.59, 99);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (655, 'Sauce - Marinara', 41.82, 135);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (656, 'Beer - True North Strong Ale', 95.69, 43);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (657, 'Veal - Tenderloin, Untrimmed', 81.03, 166);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (658, 'Soup Campbells Mexicali Tortilla', 72.52, 60);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (659, 'Tea - Decaf Lipton', 55.33, 42);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (660, 'Sauce - Sesame Thai Dressing', 4.17, 50);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (661, 'Cream - 18%', 86.31, 290);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (662, 'Rosemary - Primerba, Paste', 38.76, 39);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (663, 'Cream - 18%', 81.07, 183);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (664, 'Iced Tea - Lemon, 340ml', 59.69, 235);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (665, 'Carbonated Water - White Grape', 4.49, 109);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (666, 'Bar - Granola Trail Mix Fruit Nut', 24.29, 220);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (667, 'Wine - White, Mosel Gold', 51.13, 134);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (668, 'Tea - Grapefruit Green Tea', 7.3, 204);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (669, 'Soup - Campbells Beef Stew', 46.14, 26);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (670, 'Yogurt - Cherry, 175 Gr', 43.24, 81);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (671, 'Muffin Mix - Raisin Bran', 48.85, 186);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (672, 'Wine - Casillero Deldiablo', 38.5, 51);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (673, 'Pork - Shoulder', 7.3, 126);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (674, 'Bread Base - Italian', 92.29, 198);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (675, 'Chocolate - White', 26.31, 286);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (676, 'Glass - Juice Clear 5oz 55005', 53.89, 145);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (677, 'Paper - Brown Paper Mini Cups', 11.56, 200);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (678, 'Banana - Leaves', 57.66, 120);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (679, 'Lamb Tenderloin Nz Fr', 46.49, 99);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (680, 'Frangelico', 76.99, 289);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (681, 'Wine - Ej Gallo Sierra Valley', 10.38, 130);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (682, 'Container - Clear 32 Oz', 41.46, 288);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (683, 'Squid Ink', 96.39, 113);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (684, 'Muffin Mix - Banana Nut', 88.14, 158);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (685, 'Puree - Pear', 91.59, 89);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (686, 'Bread - White, Unsliced', 66.68, 257);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (687, 'Fiddlehead - Frozen', 64.14, 152);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (688, 'Snapple - Mango Maddness', 4.56, 193);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (689, 'Sole - Dover, Whole, Fresh', 31.54, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (690, 'Flour - Bran, Red', 65.39, 277);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (691, 'Nestea - Iced Tea', 58.66, 135);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (692, 'Cheese - Feta', 95.03, 5);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (693, 'Crab Meat Claw Pasteurise', 64.74, 182);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (694, 'Cabbage Roll', 45.56, 89);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (695, 'Lemonade - Natural, 591 Ml', 6.91, 208);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (696, 'Spoon - Soup, Plastic', 58.15, 282);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (697, 'Curry Paste - Green Masala', 58.72, 162);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (698, 'Oneshot Automatic Soap System', 31.16, 24);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (699, 'Bacardi Breezer - Strawberry', 98.35, 12);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (700, 'Wine - White, Chardonnay', 60.32, 28);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (701, 'Rum - Dark, Bacardi, Black', 89.17, 129);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (702, 'Mushroom - King Eryingii', 34.48, 100);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (703, 'Salt And Pepper Mix - White', 36.94, 268);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (704, 'Seedlings - Buckwheat, Organic', 17.1, 217);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (705, 'Kohlrabi', 28.88, 16);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (706, 'Pomello', 12.59, 22);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (707, 'Beef - Salted', 81.98, 58);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (708, 'Amaretto', 83.6, 116);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (709, 'Coconut - Shredded, Unsweet', 59.64, 40);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (710, 'Appetizer - Asian Shrimp Roll', 5.21, 162);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (711, 'Fruit Salad Deluxe', 31.55, 50);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (712, 'Molasses - Fancy', 2.71, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (713, 'Quail - Whole, Boneless', 83.76, 88);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (714, 'Quail - Jumbo', 23.72, 5);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (715, 'Oil - Grapeseed Oil', 6.85, 175);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (716, 'Nut - Almond, Blanched, Whole', 40.9, 71);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (717, 'Wine - White, Pinot Grigio', 32.88, 41);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (718, 'Pepper - Black, Whole', 11.98, 163);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (719, 'Mikes Hard Lemonade', 91.03, 257);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (720, 'Pepper - Chilli Seeds Mild', 83.54, 276);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (721, 'Foam Dinner Plate', 18.44, 183);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (722, 'Passion Fruit', 84.72, 130);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (723, 'Pastry - Mini French Pastries', 24.61, 137);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (724, 'Cream - 18%', 53.03, 187);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (725, 'Raisin - Dark', 82.99, 156);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (726, 'Nut - Walnut, Pieces', 46.61, 59);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (727, 'Port - 74 Brights', 2.31, 188);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (728, 'Quail - Whole, Boneless', 18.73, 247);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (729, 'Croissant, Raw - Mini', 56.48, 252);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (730, 'Pumpkin', 30.5, 63);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (731, 'Kellogs Cereal In A Cup', 82.36, 27);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (732, 'Trueblue - Blueberry 12x473ml', 33.7, 257);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (733, 'Oil - Hazelnut', 43.4, 286);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (734, 'Bread - Corn Muffaleta Onion', 9.8, 260);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (735, 'Bread - Pumpernickle, Rounds', 4.49, 35);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (736, 'Lamb - Shanks', 15.71, 221);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (737, 'Nut - Pine Nuts, Whole', 37.7, 115);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (738, 'Coconut - Creamed, Pure', 4.6, 64);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (739, 'Towels - Paper / Kraft', 18.33, 78);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (740, 'Wine - Sogrape Mateus Rose', 53.74, 289);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (741, 'Chocolate - Milk, Callets', 14.13, 157);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (742, 'Mushroom - Morels, Dry', 42.87, 165);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (743, 'Mix - Cocktail Strawberry Daiquiri', 34.88, 183);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (744, 'Cheese - Asiago', 90.13, 279);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (745, 'Ocean Spray - Ruby Red', 20.09, 237);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (746, 'Wine - Pinot Grigio Collavini', 98.39, 89);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (747, 'Sprouts - Alfalfa', 98.87, 16);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (748, 'Bread - Rolls, Rye', 12.37, 193);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (749, 'Soup - Beef Conomme, Dry', 66.96, 111);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (750, 'Napkin White - Starched', 29.99, 252);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (751, 'Juice - Apple, 341 Ml', 85.76, 90);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (752, 'Lettuce - Arugula', 85.43, 252);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (753, 'Mushroom - Shitake, Dry', 1.83, 154);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (754, 'Lettuce - Escarole', 73.6, 15);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (755, 'Wine - Sawmill Creek Autumn', 5.13, 69);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (756, 'Goat - Leg', 48.02, 35);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (757, 'Coriander - Seed', 81.53, 139);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (758, 'Veal - Liver', 23.28, 211);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (759, 'Appetizer - Tarragon Chicken', 5.98, 134);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (760, 'Wine - Semi Dry Riesling Vineland', 61.97, 22);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (761, 'Scallops - 20/30', 68.07, 219);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (762, 'Wine - Sherry Dry Sack, William', 64.81, 259);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (763, 'Beef - Eye Of Round', 63.05, 170);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (764, 'Pork - Loin, Boneless', 19.08, 104);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (765, 'Baking Powder', 73.06, 266);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (766, 'Carbonated Water - White Grape', 59.24, 120);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (767, 'Turnip - Wax', 31.48, 70);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (768, 'Compound - Pear', 13.05, 233);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (769, 'Pastry - Banana Muffin - Mini', 8.52, 228);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (770, 'Soup - Campbells Asian Noodle', 33.25, 142);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (771, 'Mini - Vol Au Vents', 48.76, 86);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (772, 'Nantucket Pine Orangebanana', 98.62, 16);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (773, 'Carbonated Water - Blackberry', 41.72, 95);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (774, 'Parsnip', 47.52, 186);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (775, 'Chicken - White Meat With Tender', 38.38, 240);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (776, 'Chef Hat 20cm', 95.64, 152);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (777, 'Extract - Almond', 27.16, 298);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (778, 'Wine - Penfolds Koonuga Hill', 2.26, 30);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (779, 'Pasta - Fettuccine, Dry', 58.49, 38);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (780, 'Shiro Miso', 50.66, 205);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (781, 'Jam - Raspberry,jar', 89.68, 11);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (782, 'Jam - Marmalade, Orange', 98.29, 10);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (783, 'Mousse - Mango', 15.01, 143);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (784, 'Fish - Scallops, Cold Smoked', 70.21, 2);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (785, 'Banana Turning', 18.17, 46);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (786, 'Bread - 10 Grain', 78.77, 271);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (787, 'Wine - Chateau Timberlay', 84.2, 136);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (788, 'Praline Paste', 32.85, 267);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (789, 'Maple Syrup', 79.93, 48);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (790, 'Potatoes - Mini White 3 Oz', 8.13, 86);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (791, 'Cheese - Mozzarella, Buffalo', 84.88, 220);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (792, 'Milk - Chocolate 250 Ml', 6.15, 272);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (793, 'Goat - Whole Cut', 95.06, 265);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (794, 'Lettuce - Red Leaf', 71.27, 155);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (795, 'Garbage Bag - Clear', 58.23, 141);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (796, 'Gin - Gilbeys London, Dry', 35.29, 217);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (797, 'Dawn Professionl Pot And Pan', 69.18, 137);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (798, 'Soup - Campbells, Butternut', 10.24, 207);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (799, 'Island Oasis - Peach Daiquiri', 13.0, 297);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (800, 'Croissant, Raw - Mini', 14.2, 10);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (801, 'Table Cloth 62x114 White', 51.6, 4);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (802, 'Chivas Regal - 12 Year Old', 3.14, 205);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (803, 'Wine - Taylors Reserve', 63.25, 223);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (804, 'Mushroom - Crimini', 94.88, 93);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (805, 'Versatainer Nc - 8288', 72.11, 15);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (806, 'Wine - Stoneliegh Sauvignon', 71.91, 26);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (807, 'Burger Veggie', 39.24, 157);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (808, 'Stainless Steel Cleaner Vision', 84.97, 7);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (809, 'Eggplant - Asian', 59.84, 297);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (810, 'Garam Marsala', 63.97, 148);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (811, 'Soup - Campbells Beef Strogonoff', 5.48, 101);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (812, 'Foam Espresso Cup Plain White', 24.9, 299);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (813, 'Thyme - Dried', 3.78, 282);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (814, 'Gherkin', 80.11, 245);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (815, 'Pastry - Baked Scones - Mini', 24.18, 285);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (816, 'Beef - Bresaola', 81.67, 103);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (817, 'Bread - Wheat Baguette', 75.33, 26);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (818, 'Sobe - Liz Blizz', 77.04, 109);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (819, 'Beef Flat Iron Steak', 93.35, 71);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (820, 'Crush - Grape, 355 Ml', 46.03, 154);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (821, 'Lettuce - Lolla Rosa', 29.94, 214);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (822, 'Soup - Campbells Mushroom', 5.83, 157);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (823, 'Rice Wine - Aji Mirin', 88.83, 252);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (824, 'Shrimp - Baby, Warm Water', 76.25, 242);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (825, 'Fish - Artic Char, Cold Smoked', 1.14, 163);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (826, 'Paste - Black Olive', 52.89, 276);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (827, 'Gloves - Goldtouch Disposable', 51.22, 120);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (828, 'Dried Apple', 21.41, 187);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (829, 'True - Vue Containers', 10.05, 297);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (830, 'Pastry - Chocolate Marble Tea', 95.4, 123);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (831, 'Wine - Casillero Deldiablo', 61.73, 36);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (832, 'Onions - Vidalia', 64.06, 73);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (833, 'Appetizer - Tarragon Chicken', 51.72, 221);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (834, 'Madeira', 35.78, 53);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (835, 'Puree - Kiwi', 69.37, 61);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (836, 'Cactus Pads', 58.73, 48);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (837, 'Lobster - Live', 42.13, 110);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (838, 'Lobak', 5.7, 172);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (839, 'Salmon - Atlantic, Skin On', 53.55, 234);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (840, 'Wine - Red, Cabernet Sauvignon', 2.43, 98);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (841, 'Croissants Thaw And Serve', 92.17, 208);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (842, 'Cheese Cloth', 45.11, 295);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (843, 'Apricots Fresh', 91.41, 125);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (844, 'Sage - Ground', 73.99, 145);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (845, 'Wine - Delicato Merlot', 93.02, 24);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (846, 'Rum - Cream, Amarula', 97.64, 102);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (847, 'Steam Pan - Half Size Deep', 71.21, 256);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (848, 'Goldschalger', 5.35, 133);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (849, 'Yogurt - Assorted Pack', 68.32, 160);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (850, 'Taro Root', 54.27, 32);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (851, 'Flax Seed', 91.62, 57);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (852, 'Bag - Clear 7 Lb', 85.37, 69);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (853, 'Lettuce - Belgian Endive', 48.94, 121);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (854, 'Potatoes - Idaho 100 Count', 43.15, 192);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (855, 'Crab - Claws, Snow 16 - 24', 97.13, 15);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (856, 'Tomato - Plum With Basil', 21.57, 193);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (857, 'Fudge - Chocolate Fudge', 92.57, 239);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (858, 'Breakfast Quesadillas', 74.64, 193);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (859, 'Venison - Denver Leg Boneless', 13.14, 74);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (860, 'Lumpfish Black', 25.15, 90);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (861, 'Carbonated Water - Strawberry', 9.19, 221);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (862, 'Cranberries - Frozen', 48.83, 237);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (863, 'Bread - Dark Rye', 48.7, 36);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (864, 'Soup - Campbells Beef Stew', 9.43, 175);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (865, 'Salt And Pepper Mix - Black', 88.63, 160);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (866, 'Numi - Assorted Teas', 31.71, 128);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (867, 'Assorted Desserts', 66.71, 260);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (868, 'Potatoes - Yukon Gold 5 Oz', 60.25, 209);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (869, 'Garlic - Elephant', 41.83, 268);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (870, 'Icecream Cone - Areo Chocolate', 19.57, 88);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (871, 'Soup - Campbells Beef Stew', 86.4, 87);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (872, 'Wine - Sake', 21.91, 147);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (873, 'Soup - French Can Pea', 8.64, 28);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (874, 'Nantucket Orange Juice', 8.17, 120);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (875, 'Chinese Foods - Chicken', 16.14, 138);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (876, 'Bread - Bagels, Plain', 15.93, 156);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (877, 'Wine - Cotes Du Rhone', 23.85, 104);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (878, 'Liqueur Banana, Ramazzotti', 41.07, 179);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (879, 'Flour - Whole Wheat', 55.62, 3);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (880, 'Arctic Char - Fresh, Whole', 31.67, 145);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (881, 'Stock - Beef, White', 54.51, 26);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (882, 'Sprouts Dikon', 31.69, 212);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (883, 'Truffle Cups - White Paper', 76.8, 256);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (884, 'Cream Of Tartar', 92.15, 45);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (885, 'Wine - Prosecco Valdobienne', 75.96, 200);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (886, 'Gloves - Goldtouch Disposable', 15.95, 202);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (887, 'Tamarillo', 4.99, 92);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (888, 'Bread - Ciabatta Buns', 45.67, 48);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (889, 'Bread - White, Unsliced', 93.91, 89);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (890, 'Bread - Italian Corn Meal Poly', 26.15, 48);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (891, 'Lamb - Loin, Trimmed, Boneless', 85.12, 229);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (892, 'Salmon - Atlantic, Skin On', 80.54, 64);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (893, 'Table Cloth 54x54 Colour', 99.45, 152);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (894, 'Mushroom - Shitake, Dry', 48.95, 148);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (895, 'Brandy Apricot', 51.77, 235);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (896, 'Wine - Pinot Grigio Collavini', 26.17, 53);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (897, 'Juice - Orange 1.89l', 23.9, 77);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (898, 'Tart Shells - Sweet, 2', 73.76, 153);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (899, 'Beans - Kidney, Red Dry', 56.21, 188);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (900, 'Nut - Cashews, Whole, Raw', 5.91, 81);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (901, 'Sprite, Diet - 355ml', 59.58, 208);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (902, 'Sobe - Berry Energy', 79.68, 252);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (903, 'Pork - Bones', 95.17, 42);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (904, 'Wine - Charddonnay Errazuriz', 89.76, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (905, 'Glass - Juice Clear 5oz 55005', 83.78, 245);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (906, 'Mustard - Dry, Powder', 90.38, 253);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (907, 'Pan Grease', 98.13, 200);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (908, 'Wine - Magnotta, White', 65.49, 285);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (909, 'Rice - Aborio', 41.76, 285);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (910, 'Vodka - Lemon, Absolut', 1.43, 133);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (911, 'Bag - Regular Kraft 20 Lb', 23.85, 177);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (912, 'Soup - Campbells Broccoli', 99.33, 130);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (913, 'Soup - Knorr, Classic Can. Chili', 91.16, 226);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (914, 'Danishes - Mini Cheese', 34.43, 248);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (915, 'Bread - Roll, Canadian Dinner', 49.42, 230);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (916, 'Ecolab - Medallion', 49.12, 110);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (917, 'Jagermeister', 72.56, 68);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (918, 'Table Cloth 62x114 Colour', 93.87, 252);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (919, 'Wine - Rosso Del Veronese Igt', 24.75, 229);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (920, 'Pickle - Dill', 91.91, 96);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (921, 'Juice - Happy Planet', 16.58, 44);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (922, 'Wine - Conde De Valdemar', 85.14, 294);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (923, 'Gatorade - Lemon Lime', 25.54, 105);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (924, 'Basil - Thai', 92.95, 26);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (925, 'Salt - Sea', 32.94, 61);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (926, 'Apricots - Dried', 75.87, 162);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (927, 'Kiwi', 50.49, 131);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (928, 'Wine - Magnotta - Pinot Gris Sr', 45.14, 79);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (929, 'Creme De Cacao White', 70.34, 43);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (930, 'Wine - Redchard Merritt', 63.94, 206);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (931, 'Wine - Vouvray Cuvee Domaine', 82.35, 88);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (932, 'Squeeze Bottle', 69.64, 75);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (933, 'Coconut - Creamed, Pure', 60.47, 268);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (934, 'Ecolab - Ster Bac', 57.18, 211);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (935, 'Soho Lychee Liqueur', 73.16, 41);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (936, 'Coffee - 10oz Cup 92961', 24.13, 209);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (937, 'Steel Wool S.o.s', 86.34, 278);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (938, 'Pasta - Canelloni', 51.33, 214);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (939, 'Bagel - Whole White Sesame', 62.08, 113);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (940, 'Guinea Fowl', 67.82, 102);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (941, 'Tea - Herbal I Love Lemon', 43.73, 9);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (942, 'Wine - Red, Pinot Noir, Chateau', 92.77, 72);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (943, 'Ginger - Ground', 87.21, 68);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (944, 'Brandy Apricot', 27.09, 150);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (945, 'Vegetable - Base', 54.41, 134);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (946, 'Celery Root', 83.58, 206);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (947, 'Soup - Cream Of Broccoli', 37.2, 94);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (948, 'English Muffin', 63.71, 46);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (949, 'Steam Pan - Half Size Deep', 31.27, 221);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (950, 'Muffin Mix - Banana Nut', 74.43, 170);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (951, 'Table Cloth 120 Round White', 35.63, 120);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (952, 'Cod - Salted, Boneless', 28.66, 195);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (953, 'Carrots - Purple, Organic', 56.75, 282);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (954, 'Bread - Rosemary Focaccia', 51.53, 275);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (955, 'Beans - Fava Fresh', 94.24, 31);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (956, 'Tea - English Breakfast', 99.25, 112);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (957, 'Compound - Passion Fruit', 11.44, 286);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (958, 'Crab - Imitation Flakes', 26.49, 285);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (959, 'Basil - Primerba, Paste', 13.24, 160);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (960, 'Vanilla Beans', 99.5, 186);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (961, 'Cookies - Amaretto', 61.14, 155);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (962, 'Allspice - Jamaican', 76.98, 298);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (963, 'Pepsi, 355 Ml', 15.23, 144);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (964, 'Tabasco Sauce, 2 Oz', 90.19, 181);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (965, 'Puree - Guava', 67.64, 136);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (966, 'Turkey - Ground. Lean', 74.04, 133);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (967, 'Tea - Black Currant', 31.51, 85);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (968, 'Cup Translucent 9 Oz', 92.92, 74);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (969, 'Pasta - Orzo, Dry', 4.04, 43);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (970, 'Sauce - Rosee', 24.09, 265);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (971, 'Dehydrated Kelp Kombo', 6.0, 140);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (972, 'Appetizer - Escargot Puff', 92.23, 161);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (973, 'Milk - 2% 250 Ml', 50.46, 52);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (974, 'Chicken - Wings, Tip Off', 26.16, 87);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (975, 'Spice - Greek 1 Step', 68.35, 155);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (976, 'Pastry - Trippleberry Muffin - Mini', 80.99, 8);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (977, 'Cheese - Pied De Vents', 73.59, 272);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (978, 'Spic And Span All Purpose', 36.89, 148);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (979, 'Clams - Bay', 83.81, 8);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (980, 'Beer - Original Organic Lager', 55.91, 230);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (981, 'Pasta - Lasagne, Fresh', 97.77, 10);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (982, 'Onions Granulated', 44.59, 65);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (983, 'Table Cloth 54x72 Colour', 44.56, 190);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (984, 'Wine - Zonnebloem Pinotage', 46.02, 222);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (985, 'Veal - Provimi Inside', 60.71, 255);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (986, 'Fish - Base, Bouillion', 67.06, 91);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (987, 'Juice - Ocean Spray Kiwi', 71.63, 53);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (988, 'Horseradish - Prepared', 86.1, 169);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (989, 'Water - Spring Water, 355 Ml', 21.86, 297);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (990, 'Fudge - Cream Fudge', 37.93, 278);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (991, 'Beef Dry Aged Tenderloin Aaa', 30.05, 191);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (992, 'Chicken - Whole Roasting', 97.86, 148);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (993, 'Bagelers - Cinn / Brown', 20.04, 235);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (994, 'Sauce - Roasted Red Pepper', 86.54, 267);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (995, 'Cocoa Powder - Dutched', 60.78, 154);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (996, 'Assorted Desserts', 61.33, 43);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (997, 'Cheese - Swiss Sliced', 20.07, 230);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (998, 'Cup Translucent 9 Oz', 30.77, 243);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (999, 'Wasabi Powder', 65.14, 212);
                insert into store_orderitem (id, product_title, unit_price, quantity) values (1000, 'Plastic Arrow Stir Stick', 6.89, 235);
            '''
        ]
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    for index, sql in enumerate(sql_statements, start=1):
                        cursor.execute(sql)
        except DatabaseError as e:
            for index, sql in enumerate(sql_statements[:index], start=1):
                self.stdout.write(f'Error {index}, {str(e)}')

from django.db import models


class Restaurant(models.Model):
    '''Modèle représentant un restaurant où déjeuner'''

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    website = models.URLField(blank=True, null=True)
    cuisine_type = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    price_range = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="reviews"
    )
    user_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_name} - {self.restaurant.name}"


class criteria(models.Model):
    '''criteria de notation d'un restaurant. Avec une notation de 1 à 5.'''

    criteria = [
        "Terrasse",
        "Acceuil",
        "Rapport qualité/prix",
        "RapiditéVégétarien",
        "Sans-gluten",
        "Hallal",
    ]

    name = models.CharField(max_length=100)
    comment = models.TextField()
    weight = models.DecimalField(max_digits=3, decimal_places=10, default=5.0)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="criteria"
    )

    def __str__(self):
        return self.name

    def get_weight(self):
        '''Retourne le poids du critère.'''
        return self.weight

    def set_weight(self, weight):
        '''Modifie le poids du critère.'''
        self.weight = weight

    def save(self, *args, **kwargs):
        '''Enregistre le critère.'''
        if self.weight < 0:
            raise ValueError("Le poids ne peut pas être négatif.")
        if self.weight > 5:
            raise ValueError("Le poids ne peut pas être supérieur à 5.")
        super().save(*args, **kwargs)

    def get_average_rating(self):
        '''Retourne la note moyenne du critère.'''
        ratings = statistic.objects.filter(criteria=self)
        if ratings.count() == 0:
            return 0
        total = 0
        for rating in ratings:
            total += rating.rating
        return total / ratings.count()

    def get_best_restaurant(self):
        '''Retourne le meilleur restaurant selon le critère.'''
        ratings = statistic.objects.filter(criteria=self)
        if ratings.count() == 0:
            return None
        best_rating = ratings[0]
        for rating in ratings:
            if rating.rating > best_rating.rating:
                best_rating = rating
        return rating.restaurant

    def get_worst_restaurant(self):
        '''Retourne le pire restaurant selon le critère.'''
        ratings = statistic.objects.filter(criteria=self)
        if ratings.count() == 0:
            return None
        worst_rating = ratings[0]
        for rating in ratings:
            if rating.rating < worst_rating.rating:
                worst_rating = rating
        return rating.restaurant

    def get_best_restaurant_by_criteria(self):
        '''Retourne le meilleur restaurant selon le critère.'''
        ratings = statistic.objects.filter(criteria=self)
        if ratings.count() == 0:
            return None
        best_rating = ratings[0]
        for rating in ratings:
            if rating.rating > best_rating.rating:
                best_rating = rating
        return rating.restaurant

    def get_worst_restaurant_by_criteria(self):
        '''Retourne le pire restaurant selon le critère.'''
        ratings = statistic.objects.filter(criteria=self)
        if ratings.count() == 0:
            return None
        worst_rating = ratings[0]
        for rating in ratings:
            if rating.rating < worst_rating.rating:
                worst_rating = rating
        return rating.restaurant

    def get_average_rating_by_criteria(self):
        '''Retourne la note moyenne du critère.'''
        ratings = statistic.objects.filter(criteria=self)
        if ratings.count() == 0:
            return 0
        total = 0
        for rating in ratings:
            total += rating.rating
        return total / ratings.count()


class User(models.Model):
    '''Utilisateurs de l'application, ils peuvent noter les restaurants. Ajouter leur critère.'''

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username


class statistic(models.Model):
    '''Statistiques sur l'évolution des notes d'un restaurant.
    Nous devons pouvoir l'évolution des criteria pour chaque restaurant.'''

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="statistics"
    )
    date = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    criteria = models.ForeignKey(
        criteria, on_delete=models.CASCADE, related_name="statistics"
    )

    def __str__(self):
        return f"{self.restaurant.name} - {self.date}"


cuisine_type_choices = [
    ("Français", "Français"),
    ("Italien", "Italien"),
    ("Chinois", "Chinois"),
    ("Japonais", "Japonais"),
    ("Indien", "Indien"),
    ("Mexicain", "Mexicain"),
    ("Thai", "Thai"),
    ("Américain", "Américain"),
]


class RestaurantCuisine(models.Model):
    '''Modèle représentant un type de cuisine.'''

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="cuisines"
    )
    cuisine_type = models.CharField(max_length=100, choices=cuisine_type_choices)

    def __str__(self):
        return f"{self.restaurant.name} - {self.cuisine_type}"

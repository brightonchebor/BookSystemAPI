from rest_framework import serializers
from .models Book, MonetaryDonation, DonationCampaign

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('donor', 'timestamp')

    class MonetarySerializer(serializers.ModelSerializer):
        class Meta:
            model = MonetaryDonation
            fields = '__all__'
            read_only_fields = ('donor', 'timestamp')

        class DonationCampaignSerializer(serializers.ModelSerializer):
            class Meta:
                model = DonationCampaign
                fields = '__all__'
                

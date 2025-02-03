from rest_framework import serializers
from .models import Book, MonetaryDonation, DonationCampaign

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ('donor', 'timestamp')

class MonetaryDonationSerializer(serializers.ModelSerializer):
        class Meta:
            model = MonetaryDonation
            fields = '__all__'
            read_only_fields = ('donor', 'timestamp')

class DonationCampaignSerializer(serializers.ModelSerializer):
            total_amount_raised = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

            class Meta:
                model = DonationCampaign
                fields = ['id', 'title','description','target_amount','current_amount','total_amount_raised']

            def get_total_amount_raised(self, obj):
                  return obj.current_amount()
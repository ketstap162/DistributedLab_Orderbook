from django import forms

from trading_app.models import Order


class DepositForm(forms.Form):
    amount = forms.FloatField(min_value=0.01, step_size=0.01)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Withdraw must be greater than zero")
        return amount


class WithdrawForm(forms.Form):
    amount = forms.FloatField(min_value=0.01, step_size=0.01)

    def __init__(self, *args, **kwargs):
        self.wallet = kwargs.pop('wallet')
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Withdraw must be greater than zero.")
        if amount > self.wallet.balance:
            raise forms.ValidationError("Your balance does not allow you to withdraw such an amount.")
        return amount


class OrderForm(forms.ModelForm):
    price_options = (
        ("price_per_unit", "Price for 1.0"),
        ("total_price", "Total price"),
    )
    price_option = forms.ChoiceField(
        widget=forms.RadioSelect,
        choices=price_options,
        initial="price_per_unit"
    )
    amount = forms.FloatField(min_value=0.01, step_size=0.01)
    price = forms.FloatField(min_value=0.01, step_size=0.01)

    def clean(self):
        cleaned_data = super().clean()
        wallet_from = cleaned_data.get("wallet_from")
        wallet_to = cleaned_data.get("wallet_to")
        amount = cleaned_data.get("amount")
        price = cleaned_data.get("price")
        price_option = cleaned_data.get("price_option")

        if wallet_from == wallet_to:
            raise forms.ValidationError("Wallets cannot be the same.")

        if amount <= 0:
            self.add_error("amount", "Amount must be greater than zero")

        if price <= 0:
            self.add_error("price", "Price must be greater than zero")

        if price_option == "total_price":
            price_per_unit = price / amount
            if price_per_unit < 0.01:
                self.add_error("price", "Price per unit must be >= 0.01")

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero")
        return amount

    def clean_price(self):
        price = self.cleaned_data["price"]
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero")

        return price

    def __init__(self, user, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields["wallet_from"].queryset = user.wallets.all()
        self.fields["wallet_to"].queryset = user.wallets.all()

    class Meta:
        model = Order
        fields = ["wallet_from", "wallet_to", "amount", "price"]


class OrderPurchaseForm(forms.ModelForm):
    amount = forms.FloatField(
        min_value=0.01,
        step_size=0.01,
        label="Base Amount",
    )

    def clean(self):
        cleaned_data = super().clean()
        wallet_from = cleaned_data.get("wallet_from")
        wallet_to = cleaned_data.get("wallet_to")
        order = self.order

        if wallet_from == wallet_to:
            raise forms.ValidationError("Wallets cannot be the same.")

        if order.wallet_to.currency != wallet_from.currency:
            raise forms.ValidationError(
                "The paying wallet must be of the same currency as the quote currency wallet."
            )

        if order.wallet_from.currency != wallet_to.currency:
            raise forms.ValidationError(
                "The receiving wallet must be of the same currency as the base currency wallet."
            )

    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        order_rest = self.order.rest

        if amount <= 0:
            raise forms.ValidationError("Withdraw must be greater than zero")

        if order_rest < amount:
            raise forms.ValidationError("You cannot exchange more currency than specified in the order.")
        return amount

    def __init__(self, user, order, *args, **kwargs):
        super(OrderPurchaseForm, self).__init__(*args, **kwargs)
        self.fields["wallet_from"].queryset = user.wallets.filter(currency=order.wallet_to.currency)
        self.fields["wallet_to"].queryset = user.wallets.filter(currency=order.wallet_from.currency)
        self.order = order

    class Meta:
        model = Order
        fields = ["wallet_from", "wallet_to", "amount"]

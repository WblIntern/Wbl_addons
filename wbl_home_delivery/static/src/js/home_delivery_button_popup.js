/** @odoo-module */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useRef, onMounted, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { PosStore } from "@point_of_sale/app/store/pos_store";
import { DatePickerPopup } from "@point_of_sale/app/utils/date_picker_popup/date_picker_popup";
import { DatePicker } from "@web/core/datetime/datetime_picker"

export class HomeDeliveryButtonPopup extends AbstractAwaitablePopup {
   static template = "custom_popup.HomeDeliveryPopup";
   static defaultProps = {
       closePopup: _t("Cancel"),
       confirmText: _t("Apply"),
       title: _t("Customer Home Delivery Order"),
   };
   setup() {
       super.setup();
       this.pos = usePos();
       this.rpc = useService("rpc");
       this.pos.home_delivery_delivery_date = "";
       this.pos.home_delivery_delivery_time = "";
       this.pos.home_delivery_delivery_by = "";
       this.popup = useService("popup");
       var current_pos_order = this.pos.get_order();
       this.pos.default_name = current_pos_order.partner.name
       this.pos.default_email = current_pos_order.partner.email
       this.pos.default_city = current_pos_order.partner.city
       this.pos.default_address = current_pos_order.partner.address
       this.pos.default_zip = current_pos_order.partner.zip
       this.pos.default_phone = current_pos_order.partner.phone

   };


   onClickClear() {
     $('#delivery_name').val('');
     $('#delivery_mobile').val('');
     $('#delivery_email').val('');
     $('#delivery_locality').val('');
     $('#delivery_street').val('');
     $('#delivery_city').val('');
     $('#delivery_zip').val('');
     $('#delivery_note').val('');
     $('#delivery_date').val('');
     $('#delivery_time').val('');

     this.pos.home_delivery_delivery_date = "";
     this.pos.home_delivery_delivery_time = "";
     this.pos.home_delivery_delivery_by = "";
     this.pos.is_home_delivery = "";
     this.pos.selected_delivery_instruction_note = "";
     $('#wbl_delivery_dates').val('');
     $('#selected_option_time').text('');
     this.pos.selected_weekday = "";
     this.pos.delivery_person_id = "";
     $('#selected_option').text('');
     this.pos.delivery_time_slot = "";
   };
   onClickCancel() {
       this.cancel();
       this.pos.home_delivery_delivery_date = "";
       this.pos.home_delivery_delivery_time = "";
       this.pos.home_delivery_delivery_by = "";
       this.pos.is_home_delivery = "False";
       this.pos.selected_delivery_instruction_note = "";
       $('#wbl_delivery_dates').val('');
       $('#selected_option_time').text('');
       this.pos.selected_weekday = "";
       this.pos.delivery_person_id = "";
       $('#selected_option').text('');
       this.pos.showScreen("ProductScreen");
       $('.change_color').css({
             'background-color': '',
              'color': ''
       });
   };
   onClickCreate(){
     var new_address =  $('#address_data').val();
     var delivery_name =  $('#delivery_name').val();
     var delivery_mobile =  $('#delivery_mobile').val();
     var delivery_email =  $('#delivery_email').val();
     var delivery_locality =  $('#delivery_locality').val();
     var delivery_street =  $('#delivery_street').val();
     var delivery_city =  $('#delivery_city').val();
     var delivery_zip =  $('#delivery_zip').val();
     var cashier = this.pos.pos_session.user_id[1];
     var delivery_note = $('#delivery_note').val();
     var delivery_date = $('#wbl_delivery_dates').val();
     var delivery_time = $('#delivery_time').val();
     delivery_time = delivery_date + " " + delivery_time;
     var is_home_delivery = "true";
     var current_pos_order = this.pos.get_order();
     this.pos.home_delivery_delivery_date = delivery_date;
     this.pos.home_delivery_delivery_time = delivery_time;
     this.pos.is_home_delivery = "True";
     var home_delivery_time  = this.pos.home_delivery_timing;
     var home_delivery_date  = delivery_date;

     const delivery_instruction_note = document.getElementById('delivery_instruction_note');
     const selected_delivery_instruction_note = delivery_instruction_note.options[delivery_instruction_note.selectedIndex].value;
     this.pos.selected_delivery_instruction_note = selected_delivery_instruction_note;
     this.pos.current_delivery_note = delivery_note;
     this.pos.current_delivery_instruction = selected_delivery_instruction_note;
     this.pos.current_is_home_delivery = "True";
    $('.change_color').css({
        'background-color': '#71639e',
        'color': 'white'
    });

     this.rpc("/home/delivery",{
        delivery_name : delivery_name,
        delivery_mobile : delivery_mobile,
        delivery_email : delivery_email,
        delivery_locality : delivery_locality,
        delivery_street : delivery_street,
        delivery_city : delivery_city,
        delivery_zip : delivery_zip,
        cashier : cashier,
        delivery_note : delivery_note,
        delivery_date : delivery_time,
        order_date : delivery_date,
        is_home_delivery : is_home_delivery,
        delivery_instruction_note : this.pos.selected_delivery_instruction_note,
        selected_customer_partner_id : this.pos.selectedOrder.partner.id,
        new_address : new_address,
        delivery_person_id : this.pos.delivery_person_id,
        home_delivery_time : home_delivery_time,
        home_delivery_date : home_delivery_date

     }).then(response => {
        if (response) {
            this.pos.showScreen("ProductScreen");
        }
        }).catch(error => {
            console.error("Error sending data:", error);
        });
     this.confirm();
   }

   selectDeliveryPerson(){
        const selectElement = document.getElementById('delivery_person');
        var deliveryPersons = this.pos.delivery_person.filter(person => person.is_publish);
        selectElement.innerHTML = '<option value=""></option>';
        deliveryPersons.forEach(person => {
            const option = document.createElement('option');
            option.value = person.id;
            option.textContent = person.user[1];
            selectElement.appendChild(option);
        });
        selectElement.addEventListener('change', () => {
            const selectedValue = selectElement.value;
            this.pos.delivery_person_id = selectedValue
            const selectedText = selectElement.options[selectElement.selectedIndex].text;
            $("#selected_option").text(selectedText);
            this.pos.home_delivery_delivery_by = selectedText;
               const selected_delivery_person = this.pos.delivery_person.filter(delivery_person => delivery_person.id == this.pos.delivery_person_id);
               this.pos.delivery_time_slot  = selected_delivery_person[0].delivery_time_slot;
               this.pos.selected_delivery_person_delivery_date = selected_delivery_person[0].delivery_date;
               $('#wbl_delivery_dates').val('');
               $('#selected_option_time').text('');
               this.pos.selected_weekday = "";
               this._onCarrierClick();
        });
   }

   selectDeliveryTiming(){
        const selectElement = document.getElementById('delivery_person_time');
        const selected_delivery_person = this.pos.delivery_person.filter(delivery_person => delivery_person.id == this.pos.delivery_person_id);
        var order_preparing_time = selected_delivery_person[0].order_preparation_time;
        var selected_delivery_time_schedule = this.pos.delivery_time_schedule.filter(time_schedule =>time_schedule.delivery_carrier_id[0] ==  this.pos.delivery_person_id)
        var final_selected_delivery_time_schedule = selected_delivery_time_schedule.filter(final_time_schedule =>final_time_schedule.week_days ==  this.pos.selected_weekday)
        if(final_selected_delivery_time_schedule && final_selected_delivery_time_schedule[0].open_time_hours) {
            var time_interval = selected_delivery_person[0].time_interval;
            var open_time_hours =  final_selected_delivery_time_schedule[0].open_time_hours;
            var close_time_hours =  final_selected_delivery_time_schedule[0].close_time_hours;
            var open_time_minutes =  final_selected_delivery_time_schedule[0].open_time_minutes;
            var close_time_minutes = final_selected_delivery_time_schedule[0].close_time_minutes;
            var total_hours = Math.abs(open_time_hours - close_time_hours);
            var total_minutes = (total_hours * 60)  + parseInt(open_time_minutes) + parseInt(close_time_minutes)
            var hours = Math.floor(total_minutes / 60);
            var totalMinutes = total_minutes;
            var interval = time_interval;
            var startHour = open_time_hours;
            function formatHour(hour) {
                return hour % 24;
            }
            var timeSlots = [];
            var currentStartTime = startHour * 60;
            while (currentStartTime < (startHour * 60 + totalMinutes)) {
                var startTime = currentStartTime;
                var endTime = currentStartTime + interval;
                var startHourFormatted = formatHour(Math.floor(startTime / 60));
                var endHourFormatted = formatHour(Math.floor(endTime / 60));
                var timeSlot = `${startHourFormatted}-${endHourFormatted}`;
                timeSlots.push(timeSlot);
                currentStartTime = endTime;
            }
            var deliveryPersonsTiming = timeSlots;
            var home_delivery_time  = this.pos.home_delivery_timing;
            var home_delivery_date  = $('#wbl_delivery_dates').val();

            const currentTime = new Date();
            let current_hours = currentTime.getHours();
            const current_minutes = currentTime.getMinutes();
            const current_seconds = currentTime.getSeconds();
            const ampm = current_hours >= 12 ? 'PM' : 'AM';
            current_hours = current_hours % 12;
            current_hours = current_hours ? current_hours : 12; // the hour '0' should be '12'
            const current_formattedTime = `${current_hours < 10 ? '0' : ''}${current_hours}:${current_minutes < 10 ? '0' : ''}${current_minutes} ${ampm}`;

            var home_delivery_person_id =  selected_delivery_person[0].id;
            this.rpc("/slot_check",{
               available_slots : deliveryPersonsTiming,
               home_delivery_time : home_delivery_time,
               home_delivery_date : home_delivery_date,
               home_delivery_person_id : home_delivery_person_id,
               current_time : current_formattedTime,
               order_preparing_time : order_preparing_time
            }).then(response => {
            if (response) {
                selectElement.innerHTML = '<option value=""></option>';
                response.available_slots.forEach(Timing => {
                    const option = document.createElement('option');
                    option.value = Timing;
                    option.textContent = Timing;
                    selectElement.appendChild(option);
                });
                selectElement.addEventListener('change', () => {
                    const selectedValue = selectElement.value;
                    const selectedText = selectElement.options[selectElement.selectedIndex].text;
                    $("#selected_option_time").text(selectedText);
                    this.pos.home_delivery_timing = selectedText;
                    $('#slot_timing').text(selectedText);
                    this.pos.selected_time= selectElement.value;
                });
            this.pos.slot_selection = response.available_slots;
            }
            }).catch(error => {
                console.error("Error sending data:", error);
            });
        }
        const print_selected_delivery_person = this.pos.delivery_person.filter(delivery_person => delivery_person.id == this.pos.delivery_person_id);
        const print_person_name = document.getElementById('delivery_person');
        print_person_name.innerHTML = `<option value="">${ print_selected_delivery_person[0].user[1]}</option>`;

        if (this.pos.selected_time){
                 const selected_slot = this.pos.slot_selection.filter(slot => slot == this.pos.selected_time);
                const print_time = document.getElementById('delivery_person_time');
                print_time.innerHTML = `<option value="">${ selected_slot}</option>`;
        }

   }

   _onCarrierClick() {
        $("#wbl_delivery_dates").datepicker("destroy");
        var pos = this.pos;
        const selected_delivery_person = this.pos.delivery_person.filter(delivery_person => delivery_person.id == this.pos.delivery_person_id);
        var today = new Date();
        today.setDate(today.getDate() + selected_delivery_person[0].start_day_after);
        var year = today.getFullYear();
        var month = (today.getMonth() + 1).toString().padStart(2, '0');
        var day = today.getDate().toString().padStart(2, '0');
        var formattedDate = `${year}-${month}-${day}`;
        var allowed_weekdays = this.pos.delivery_time_schedule
            .filter(item => item.delivery_carrier_id[0] == this.pos.delivery_person_id)
            .map(item => item.week_days);
        var allowed_days = allowed_weekdays.map(function(day) {
            switch(day) {
                case 'Sunday': return 0;
                case 'Monday': return 1;
                case 'Tuesday': return 2;
                case 'Wednesday': return 3;
                case 'Thursday': return 4;
                case 'Friday': return 5;
                case 'Saturday': return 6;
                default: return -1;
            }
        });

        $("#wbl_delivery_dates").datepicker({
            dateFormat: "yy/mm/dd",
            minDate: today,
            beforeShowDay: function(date) {
                var dayOfWeek = date.getDay();
                if (allowed_days.indexOf(dayOfWeek) === -1) {
                    return [false];
                }
                return [true];
            },
            onSelect: function(dateText, inst) {
                var selectedDate = new Date(inst.selectedYear, inst.selectedMonth, inst.selectedDay);
                var dayNames = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
                var dayName = dayNames[selectedDate.getDay()];
                $('#selected_option_time').text('');
                pos.selected_weekday = dayName;
            }
        });
        $("#wbl_delivery_dates").datepicker("show");
   }

   onClickAddress(){
     var selectedValue = $('input[name="address"]:checked').val();
        const deliveryFields = document.querySelector('.delivery-fields');
       const default_information = document.querySelector('.default_information');
     if (selectedValue == "new_address"){
           default_information.style.display = 'none';
            deliveryFields.style.display = 'block';
             this.value = "True";
             $('#address_data').val('True');
     }
     else{
          deliveryFields.style.display = 'none';
          default_information.style.display = 'block';
          $('#address_data').val('False');
     }


   }

}


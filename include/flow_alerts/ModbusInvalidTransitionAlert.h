/*
 *
 * (C) 2013-24 - ntop.org
 *
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software Foundation,
 * Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 */

#ifndef _Modbus_INVALID_TRANSITION_ALERT_H_
#define _Modbus_INVALID_TRANSITION_ALERT_H_

#include "ntop_includes.h"

class ModbusInvalidTransitionAlert : public FlowAlert {
 private:
  u_int32_t packet_epoch;
  u_int16_t type_i;
  u_int8_t type_id;

  ndpi_serializer *getAlertJSON(ndpi_serializer *serializer);

 public:
  static FlowAlertType getClassType() {
    return {flow_alert_modbus_invalid_transition, alert_category_security};
  }
  static u_int8_t getDefaultScore() { return SCORE_LEVEL_NOTICE; };

  inline u_int32_t get_packet_epoch() { return packet_epoch; };
  inline u_int16_t get_type_i() { return type_i; };
  inline u_int8_t get_type_id() { return type_id; };

  ModbusInvalidTransitionAlert(FlowCheck *c, Flow *f, struct timeval *_time,
			       u_int16_t _type_i, u_int8_t _type_id) : FlowAlert(c, f) {
    type_i = _type_i;
    type_id = _type_id;
    packet_epoch = _time->tv_sec;
    setAlertScore(getDefaultScore());
  };
  ~ModbusInvalidTransitionAlert(){};

  bool autoAck() const { return false; };

  FlowAlertType getAlertType() const { return getClassType(); }
};

#endif /* _Modbus_INVALID_TRANSITION_ALERT_H_ */

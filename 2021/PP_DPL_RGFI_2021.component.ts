import { ChangeDetectorRef, Component } from '@angular/core'
import { Obrazac } from "../obrazac";
import { BackendServiceService } from "../../backend-service.service";

@Component({
  selector: 'PP_DPL_RGFI_2021',
  templateUrl: 'PP_DPL_RGFI_2021.component.html',
})
export class PP_DPL_RGFI_2021 extends Obrazac {

  constructor(_backendService: BackendServiceService,
    _cd: ChangeDetectorRef) {
    super(_backendService, _cd);
  }
}
